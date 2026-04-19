{{/*
Expand the name of the chart.
*/}}
{{- define "hackathon-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "hackathon-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "hackathon-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "hackathon-app.labels" -}}
helm.sh/chart: {{ include "hackathon-app.chart" . }}
{{ include "hackathon-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "hackathon-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "hackathon-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "hackathon-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "hackathon-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Backend fullname
*/}}
{{- define "hackathon-app.backend.fullname" -}}
{{- printf "%s-backend" (include "hackathon-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "hackathon-app.backend.labels" -}}
{{ include "hackathon-app.labels" . }}
app.kubernetes.io/component: backend
app.kubernetes.io/name: {{ include "hackathon-app.backend.name" . }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "hackathon-app.backend.selectorLabels" -}}
{{ include "hackathon-app.selectorLabels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Backend name
*/}}
{{- define "hackathon-app.backend.name" -}}
{{- printf "%s-backend" (include "hackathon-app.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend fullname
*/}}
{{- define "hackathon-app.frontend.fullname" -}}
{{- printf "%s-frontend" (include "hackathon-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "hackathon-app.frontend.labels" -}}
{{ include "hackathon-app.labels" . }}
app.kubernetes.io/component: frontend
app.kubernetes.io/name: {{ include "hackathon-app.frontend.name" . }}
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "hackathon-app.frontend.selectorLabels" -}}
{{ include "hackathon-app.selectorLabels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Frontend name
*/}}
{{- define "hackathon-app.frontend.name" -}}
{{- printf "%s-frontend" (include "hackathon-app.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Secret name
*/}}
{{- define "hackathon-app.secretName" -}}
{{- printf "%s-secrets" (include "hackathon-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
