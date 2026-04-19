// DatabaseAgent - Neon PostgreSQL Manager
//
// Focus: Reliable, secure, and performant management of Neon Serverless PostgreSQL databases
// Responsibilities: Connection management, schema design, query optimization, 
// performance monitoring, security implementation, migration management

const { Pool } = require('pg'); // PostgreSQL client
const dotenv = require('dotenv');

class DatabaseAgent {
  constructor(options = {}) {
    this.config = {
      // Default configuration values
      maxConnections: options.maxConnections || 10,
      idleTimeoutMillis: options.idleTimeoutMillis || 30000,
      connectionTimeoutMillis: options.connectionTimeoutMillis || 2000,
      enableMetrics: options.enableMetrics || true,
      logSlowQueries: options.logSlowQueries || true,
      slowQueryThreshold: options.slowQueryThreshold || 1000, // 1 second
      ...options
    };

    // Initialize database pools for different environments
    this.pools = {};
    this.metrics = {};
    this.queryHistory = [];
    
    // Load environment variables
    dotenv.config();
  }

  // Initialize connection pools for different environments
  async initializePools(environments = ['development', 'staging', 'production']) {
    for (const env of environments) {
      const connectionString = process.env[`DATABASE_URL_${env.toUpperCase()}`] || 
                              process.env.DATABASE_URL;
      
      if (connectionString) {
        this.pools[env] = new Pool({
          connectionString,
          max: this.config.maxConnections,
          idleTimeoutMillis: this.config.idleTimeoutMillis,
          connectionTimeoutMillis: this.config.connectionTimeoutMillis,
          // Neon-specific settings
          ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
        });

        // Add connection event listeners for monitoring
        this.pools[env].on('connect', () => {
          this.incrementMetric('connections_opened', env);
        });

        this.pools[env].on('remove', () => {
          this.incrementMetric('connections_closed', env);
        });
      }
    }
    
    console.log('Database pools initialized for environments:', Object.keys(this.pools));
  }

  // Get the appropriate pool based on environment
  getPool(environment = process.env.NODE_ENV || 'development') {
    if (!this.pools[environment]) {
      throw new Error(`No database pool configured for environment: ${environment}`);
    }
    return this.pools[environment];
  }

  // Execute a query with performance monitoring
  async query(sql, params = [], environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    const startTime = Date.now();
    
    try {
      const result = await pool.query(sql, params);
      
      const duration = Date.now() - startTime;
      
      // Log slow queries if enabled
      if (this.config.logSlowQueries && duration > this.config.slowQueryThreshold) {
        console.warn(`Slow query detected (${duration}ms):`, sql.substring(0, 100) + '...');
        this.incrementMetric('slow_queries', environment);
      }
      
      // Track query performance metrics
      if (this.config.enableMetrics) {
        this.trackQueryPerformance(sql, duration, environment);
      }
      
      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      console.error(`Database query error after ${duration}ms:`, error.message);
      this.incrementMetric('failed_queries', environment);
      throw error;
    }
  }

  // Track query performance metrics
  trackQueryPerformance(sql, duration, environment) {
    const querySignature = this.getQuerySignature(sql);
    
    if (!this.metrics[environment]) {
      this.metrics[environment] = {};
    }
    
    if (!this.metrics[environment][querySignature]) {
      this.metrics[environment][querySignature] = {
        count: 0,
        totalDuration: 0,
        avgDuration: 0,
        maxDuration: 0,
        minDuration: Infinity
      };
    }
    
    const stats = this.metrics[environment][querySignature];
    stats.count++;
    stats.totalDuration += duration;
    stats.avgDuration = stats.totalDuration / stats.count;
    stats.maxDuration = Math.max(stats.maxDuration, duration);
    stats.minDuration = Math.min(stats.minDuration, duration);
    
    // Store query in history for analysis
    this.queryHistory.push({
      sql: sql.substring(0, 200), // Truncate for storage efficiency
      duration,
      environment,
      timestamp: new Date()
    });
    
    // Keep query history to a reasonable size
    if (this.queryHistory.length > 1000) {
      this.queryHistory.shift();
    }
  }

  // Get a simplified signature of the SQL query for grouping
  getQuerySignature(sql) {
    // Remove variable parts to group similar queries
    return sql
      .toLowerCase()
      .replace(/\s+/g, ' ') // Normalize whitespace
      .replace(/'.*?'/g, '?') // Replace string literals
      .replace(/\d+/g, '?') // Replace numbers
      .substring(0, 100); // Limit length
  }

  // Increment a metric counter
  incrementMetric(metricName, environment) {
    if (!this.metrics[environment]) {
      this.metrics[environment] = {};
    }
    
    if (!this.metrics[environment][metricName]) {
      this.metrics[environment][metricName] = 0;
    }
    
    this.metrics[environment][metricName]++;
  }

  // Get database performance metrics
  getMetrics(environment = process.env.NODE_ENV || 'development') {
    return this.metrics[environment] || {};
  }

  // Analyze slow queries
  getSlowQueries(environment = process.env.NODE_ENV || 'development', threshold = this.config.slowQueryThreshold) {
    return this.queryHistory
      .filter(q => q.duration > threshold && q.environment === environment)
      .sort((a, b) => b.duration - a.duration);
  }

  // Optimize a query by suggesting improvements
  async analyzeQuery(sql, environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    
    try {
      // Get the query execution plan
      const explainResult = await pool.query('EXPLAIN (ANALYZE, BUFFERS) ' + sql);
      
      const analysis = {
        query: sql,
        executionPlan: explainResult.rows,
        suggestions: []
      };
      
      // Analyze the execution plan for potential issues
      const planText = explainResult.rows.map(row => row['QUERY PLAN']).join(' ');
      
      // Check for full table scans
      if (planText.toLowerCase().includes('seq scan')) {
        analysis.suggestions.push('Consider adding an index to avoid sequential scan');
      }
      
      // Check for nested loop joins that could be hash joins
      if ((planText.toLowerCase().match(/nested loop/g) || []).length > 2) {
        analysis.suggestions.push('Multiple nested loops detected - consider rewriting to use hash joins or merge joins');
      }
      
      // Check for high buffer usage
      if (planText.toLowerCase().includes('buffers:')) {
        const buffersMatch = planText.match(/buffers:.*?temp=(\d+)/i);
        if (buffersMatch && parseInt(buffersMatch[1]) > 10000) {
          analysis.suggestions.push('High temporary buffer usage detected - consider optimizing the query or increasing work_mem');
        }
      }
      
      return analysis;
    } catch (error) {
      console.error('Error analyzing query:', error.message);
      throw error;
    }
  }

  // Create a database schema
  async createSchema(schemaDefinition, environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    
    // Begin transaction
    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      
      // Create tables based on schema definition
      for (const table of schemaDefinition.tables) {
        const columns = table.columns.map(col => {
          let colDef = `"${col.name}" ${col.type}`;
          if (col.primaryKey) colDef += ' PRIMARY KEY';
          if (col.notNull) colDef += ' NOT NULL';
          if (col.unique) colDef += ' UNIQUE';
          if (col.defaultValue !== undefined) colDef += ` DEFAULT ${col.defaultValue}`;
          if (col.references) colDef += ` REFERENCES "${col.references.table}"("${col.references.column}")`;
          return colDef;
        }).join(', ');
        
        const createTableQuery = `CREATE TABLE IF NOT EXISTS "${table.name}" (${columns})`;
        await client.query(createTableQuery);
      }
      
      // Create indexes
      if (schemaDefinition.indexes) {
        for (const index of schemaDefinition.indexes) {
          const indexQuery = `CREATE INDEX IF NOT EXISTS "${index.name}" ON "${index.table}" (${index.columns.map(c => `"${c}"`).join(', ')})`;
          await client.query(indexQuery);
        }
      }
      
      // Commit transaction
      await client.query('COMMIT');
      
      console.log(`Schema created successfully in ${environment} environment`);
      return { success: true, message: 'Schema created successfully' };
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error creating schema:', error.message);
      throw error;
    } finally {
      client.release();
    }
  }

  // Execute a database migration
  async executeMigration(migration, environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    
    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      
      // Execute migration steps
      for (const step of migration.steps) {
        await client.query(step.sql, step.params || []);
      }
      
      // Mark migration as completed
      const insertMigration = `
        INSERT INTO schema_migrations (version, name, applied_at) 
        VALUES ($1, $2, NOW())
        ON CONFLICT (version) DO NOTHING`;
      
      await client.query(insertMigration, [migration.version, migration.name]);
      
      await client.query('COMMIT');
      
      console.log(`Migration ${migration.version} applied successfully in ${environment} environment`);
      return { success: true, version: migration.version, message: 'Migration applied successfully' };
    } catch (error) {
      await client.query('ROLLBACK');
      console.error(`Error applying migration ${migration.version}:`, error.message);
      throw error;
    } finally {
      client.release();
    }
  }

  // Create a database migration table if it doesn't exist
  async ensureMigrationTable(environment = process.env.NODE_ENV || 'development') {
    const createTableQuery = `
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )`;
    
    await this.query(createTableQuery, [], environment);
  }

  // Get pending migrations
  async getPendingMigrations(allMigrations, environment = process.env.NODE_ENV || 'development') {
    // First ensure the migration table exists
    await this.ensureMigrationTable(environment);
    
    // Get applied migrations
    const appliedResult = await this.query(
      'SELECT version FROM schema_migrations ORDER BY version',
      [],
      environment
    );
    
    const appliedVersions = appliedResult.rows.map(r => r.version);
    return allMigrations.filter(m => !appliedVersions.includes(m.version));
  }

  // Optimize database by running ANALYZE and VACUUM
  async optimizeDatabase(tables = [], environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    
    const client = await pool.connect();
    try {
      // If no specific tables provided, optimize the entire database
      if (tables.length === 0) {
        await client.query('ANALYZE');
        console.log('Database ANALYZE completed');
      } else {
        // Optimize specific tables
        for (const table of tables) {
          await client.query(`ANALYZE "${table}"`);
          console.log(`ANALYZE completed for table: ${table}`);
        }
      }
      
      return { success: true, message: 'Database optimization completed' };
    } catch (error) {
      console.error('Error optimizing database:', error.message);
      throw error;
    } finally {
      client.release();
    }
  }

  // Create an index with performance considerations
  async createIndex(tableName, columnName, options = {}, environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    
    const indexName = `${tableName}_${columnName}_idx`;
    const unique = options.unique ? 'UNIQUE' : '';
    const method = options.method || 'B-TREE'; // Default to B-tree
    
    const createIndexQuery = `
      CREATE ${unique} INDEX CONCURRENTLY IF NOT EXISTS "${indexName}" 
      ON "${tableName}" USING ${method} ("${columnName}")
    `;
    
    try {
      await pool.query(createIndexQuery);
      console.log(`Index ${indexName} created successfully`);
      return { success: true, indexName };
    } catch (error) {
      console.error(`Error creating index ${indexName}:`, error.message);
      throw error;
    }
  }

  // Check for unused indexes
  async findUnusedIndexes(environment = process.env.NODE_ENV || 'development') {
    const unusedIndexesQuery = `
      SELECT 
        schemaname, 
        tablename, 
        indexname, 
        idx_scan
      FROM pg_stat_user_indexes 
      WHERE schemaname = 'public' AND idx_scan = 0
    `;
    
    const result = await this.query(unusedIndexesQuery, [], environment);
    return result.rows;
  }

  // Close all database connections
  async closeAllPools() {
    const closePromises = Object.values(this.pools).map(pool => pool.end());
    await Promise.all(closePromises);
    console.log('All database pools closed');
  }

  // Health check for database connectivity
  async healthCheck(environment = process.env.NODE_ENV || 'development') {
    try {
      const pool = this.getPool(environment);
      const result = await pool.query('SELECT 1 as alive');
      
      return {
        status: 'healthy',
        environment,
        ping: result.rows[0].alive
      };
    } catch (error) {
      console.error(`Health check failed for ${environment}:`, error.message);
      return {
        status: 'unhealthy',
        environment,
        error: error.message
      };
    }
  }

  // Get connection pool statistics
  getConnectionStats(environment = process.env.NODE_ENV || 'development') {
    const pool = this.getPool(environment);
    if (!pool) {
      return null;
    }
    
    return {
      totalConnections: pool.totalCount,
      idleConnections: pool.idleCount,
      waitingClients: pool.waitingCount,
      maxConnections: this.config.maxConnections
    };
  }

  // Monitor database for potential issues
  async monitorDatabase(environment = process.env.NODE_ENV || 'development') {
    const issues = [];
    
    // Check connection pool health
    const stats = this.getConnectionStats(environment);
    if (stats) {
      if (stats.waitingClients > 0) {
        issues.push(`Connection pool congestion: ${stats.waitingClients} clients waiting`);
      }
      
      if (stats.idleConnections === 0) {
        issues.push('No idle connections available');
      }
    }
    
    // Check for slow queries
    const slowQueries = this.getSlowQueries(environment);
    if (slowQueries.length > 5) { // More than 5 slow queries recently
      issues.push(`High number of slow queries detected: ${slowQueries.length}`);
    }
    
    // Check for unused indexes
    try {
      const unusedIndexes = await this.findUnusedIndexes(environment);
      if (unusedIndexes.length > 0) {
        issues.push(`Found ${unusedIndexes.length} potentially unused indexes`);
      }
    } catch (error) {
      console.error('Error checking for unused indexes:', error.message);
    }
    
    return {
      environment,
      timestamp: new Date(),
      issues,
      stats
    };
  }
}

module.exports = DatabaseAgent;