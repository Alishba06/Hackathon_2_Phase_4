"""
Security log analysis tools for the Todo application.

This module provides functions for analyzing security logs
to identify potential threats and anomalies.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
import logging

from ..models.security_log import SecurityLog, SecurityEventType
from ..models.user import User
from ..config.database import engine
from sqlmodel import Session, select


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_security_logs_by_timeframe(start_time: datetime, end_time: datetime) -> Dict[str, any]:
    """
    Analyze security logs within a specific timeframe.
    
    Args:
        start_time: Start of the analysis period
        end_time: End of the analysis period
    
    Returns:
        Dictionary with analysis results
    """
    with Session(engine) as session:
        statement = select(SecurityLog).where(
            SecurityLog.timestamp >= start_time,
            SecurityLog.timestamp <= end_time
        )
        logs = session.exec(statement).all()
        
        # Count events by type
        event_counts = defaultdict(int)
        user_activity = defaultdict(list)
        ip_addresses = defaultdict(int)
        
        for log in logs:
            event_counts[log.event_type.value] += 1
            if log.user_id:
                user_activity[log.user_id].append(log)
            if log.ip_address:
                ip_addresses[log.ip_address] += 1
        
        # Identify potential threats
        suspicious_ips = [ip for ip, count in ip_addresses.items() if count > 10]  # Threshold configurable
        high_risk_events = [event_type for event_type, count in event_counts.items() 
                           if event_type in [SecurityEventType.AUTH_FAILURE, 
                                           SecurityEventType.UNAUTHORIZED_ACCESS,
                                           SecurityEventType.USER_ISOLATION_VIOLATION]]
        
        return {
            "total_events": len(logs),
            "event_counts": dict(event_counts),
            "user_activity": {user_id: len(activity) for user_id, activity in user_activity.items()},
            "suspicious_ips": suspicious_ips,
            "high_risk_events": high_risk_events,
            "timeframe": {"start": start_time.isoformat(), "end": end_time.isoformat()}
        }


def detect_brute_force_attempts(user_id: str, timeframe_minutes: int = 15) -> List[SecurityLog]:
    """
    Detect potential brute force attempts for a specific user.
    
    Args:
        user_id: ID of the user to check
        timeframe_minutes: Time window in minutes to check for attempts
    
    Returns:
        List of security logs that may indicate brute force attempts
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=timeframe_minutes)
    
    with Session(engine) as session:
        statement = select(SecurityLog).where(
            SecurityLog.user_id == user_id,
            SecurityLog.event_type == SecurityEventType.AUTH_FAILURE,
            SecurityLog.timestamp >= start_time,
            SecurityLog.timestamp <= end_time
        ).order_by(SecurityLog.timestamp.desc())
        
        auth_failures = session.exec(statement).all()
        
        # If there are more than 5 failures in the timeframe, flag as potential brute force
        if len(auth_failures) > 5:
            logger.warning(f"Potential brute force attempt detected for user {user_id}")
            return auth_failures
        else:
            return []


def detect_ip_based_threats(ip_address: str, timeframe_hours: int = 1) -> Dict[str, any]:
    """
    Detect potential threats from a specific IP address.
    
    Args:
        ip_address: IP address to analyze
        timeframe_hours: Time window in hours to check for suspicious activity
    
    Returns:
        Dictionary with threat assessment
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=timeframe_hours)
    
    with Session(engine) as session:
        statement = select(SecurityLog).where(
            SecurityLog.ip_address == ip_address,
            SecurityLog.timestamp >= start_time,
            SecurityLog.timestamp <= end_time
        )
        logs = session.exec(statement).all()
        
        event_counts = defaultdict(int)
        users_targeted = set()
        
        for log in logs:
            event_counts[log.event_type.value] += 1
            if log.user_id:
                users_targeted.add(log.user_id)
        
        # Assess risk based on event types and frequency
        auth_failures = event_counts.get(SecurityEventType.AUTH_FAILURE.value, 0)
        unauthorized_access = event_counts.get(SecurityEventType.UNAUTHORIZED_ACCESS.value, 0)
        user_isolation_violations = event_counts.get(SecurityEventType.USER_ISOLATION_VIOLATION.value, 0)
        
        risk_score = (auth_failures * 1) + (unauthorized_access * 2) + (user_isolation_violations * 3)
        
        risk_level = "LOW"
        if risk_score > 20:
            risk_level = "HIGH"
        elif risk_score > 10:
            risk_level = "MEDIUM"
        
        return {
            "ip_address": ip_address,
            "timeframe": {"start": start_time.isoformat(), "end": end_time.isoformat()},
            "total_events": len(logs),
            "event_counts": dict(event_counts),
            "users_targeted": list(users_targeted),
            "risk_score": risk_score,
            "risk_level": risk_level
        }


def get_security_summary() -> Dict[str, any]:
    """
    Get a summary of security events.
    
    Returns:
        Dictionary with security summary
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)  # Last 24 hours
    
    with Session(engine) as session:
        statement = select(SecurityLog).where(
            SecurityLog.timestamp >= start_time,
            SecurityLog.timestamp <= end_time
        )
        all_logs = session.exec(statement).all()
        
        event_counts = defaultdict(int)
        for log in all_logs:
            event_counts[log.event_type.value] += 1
        
        # Find most active IPs
        ip_counts = defaultdict(int)
        for log in all_logs:
            if log.ip_address:
                ip_counts[log.ip_address] += 1
        
        most_active_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Find users with most security events
        user_counts = defaultdict(int)
        for log in all_logs:
            if log.user_id:
                user_counts[log.user_id] += 1
        
        most_active_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "period_start": start_time.isoformat(),
            "period_end": end_time.isoformat(),
            "total_security_events": len(all_logs),
            "event_type_breakdown": dict(event_counts),
            "most_active_ips": most_active_ips,
            "most_active_users": most_active_users
        }


def generate_security_report(days_back: int = 7) -> str:
    """
    Generate a security report for the specified number of days.
    
    Args:
        days_back: Number of days back to include in the report
    
    Returns:
        Formatted security report as a string
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days_back)
    
    analysis = analyze_security_logs_by_timeframe(start_time, end_time)
    
    report = f"""
Security Report: {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}

Total Security Events: {analysis['total_events']}

Event Type Breakdown:
"""
    for event_type, count in analysis['event_counts'].items():
        report += f"- {event_type}: {count}\n"
    
    report += f"\nSuspicious IP Addresses: {', '.join(analysis['suspicious_ips']) if analysis['suspicious_ips'] else 'None'}"
    
    report += f"\n\nHigh-Risk Event Types: {', '.join(analysis['high_risk_events']) if analysis['high_risk_events'] else 'None'}"
    
    return report


def flag_suspicious_activity():
    """
    Flag suspicious activity based on security log analysis.
    This function would typically integrate with alerting systems.
    """
    # Get logs from the last hour
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)
    
    with Session(engine) as session:
        # Look for multiple auth failures from the same IP
        statement = select(SecurityLog).where(
            SecurityLog.event_type == SecurityEventType.AUTH_FAILURE,
            SecurityLog.timestamp >= start_time,
            SecurityLog.timestamp <= end_time
        )
        auth_failures = session.exec(statement).all()
        
        # Group by IP address
        ip_failures = defaultdict(list)
        for log in auth_failures:
            if log.ip_address:
                ip_failures[log.ip_address].append(log)
        
        # Flag IPs with more than 10 failures in the last hour
        for ip, failures in ip_failures.items():
            if len(failures) > 10:
                logger.warning(f"SUSPICIOUS ACTIVITY: IP {ip} had {len(failures)} authentication failures in the last hour")
                # In a real system, this might trigger an alert or temporary IP block