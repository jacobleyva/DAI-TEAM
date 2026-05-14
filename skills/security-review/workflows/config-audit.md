---
title: Workflow — Config Audit (IaC / Cloud / Container / CI / K8s)
type: workflow
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - config-audit
  - workflow
  - iac
  - cloud
  - container
  - kubernetes
artifact_type: skill-workflow
---

# Workflow: Config Audit

Infrastructure-as-Code and configuration review. Covers cloud, container, CI/CD, and Kubernetes. Tool-verifiable throughout.

## Phase 1 — Scope

Identify what's in front of you:

- Terraform / OpenTofu / CloudFormation / Pulumi / Bicep → cloud IaC
- Dockerfile / docker-compose.yml / image manifests → container
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/` → CI/CD
- `*.yaml` with `kind:` → Kubernetes manifests
- `helm/` chart, `kustomize/` overlays → Kubernetes packaging

**Exit probe:** scope list with file count per category.

## Phase 2 — Run the Scanners

Run the appropriate scanners; keep output files as evidence.

```bash
# Polyglot IaC
checkov -d . -o json --output-file-path checkov.json

# Terraform-specific (deeper plan-aware)
tfsec . --format json --out tfsec.json
trivy config . --format json -o trivy-config.json

# Kubernetes manifests
kubescape scan . --format json --output kubescape.json
kube-score score *.yaml > kube-score.txt

# Container images (once built)
trivy image <image:tag> --format json -o trivy-image.json
grype <image:tag> -o json > grype.json
```

Triage: keep CRITICAL/HIGH; review MEDIUMs in cloud/network exposure rules.

**Exit probe:** at least one scanner ran successfully and produced output for each in-scope category.

## Phase 3 — Cloud Configuration Checklist

### IAM
- [ ] No `*:*` or `Action: "*"` policies on principals unless explicitly justified (and even then, narrow with `Condition`).
- [ ] No `Principal: "*"` on S3 buckets, KMS keys, SNS topics, Lambda invoke policies.
- [ ] Long-lived access keys absent; IAM roles + STS or workload identity (IRSA, GKE WI, Azure managed identity) used instead.
- [ ] Cross-account roles have `sts:ExternalId` requirement.
- [ ] No `iam:PassRole` allowed for `Resource: "*"`.

### Networking
- [ ] Security groups / NSG rules: no `0.0.0.0/0` on SSH (22), RDP (3389), DB ports (3306/5432/1433/27017/6379/9200) without explicit comment and compensating control.
- [ ] Default-deny egress baseline (allow specific egress only).
- [ ] Private subnets for data tier; public IPs only on documented ingress.
- [ ] VPC endpoints used for S3/DynamoDB/Secrets Manager etc. when in private subnets.

### Storage
- [ ] S3 / GCS / Azure Blob buckets: public access blocked at account + bucket level.
- [ ] Encryption at rest enabled with customer-managed keys for sensitive data.
- [ ] Versioning + MFA Delete on buckets holding logs or audit-relevant data.
- [ ] Lifecycle policies move/expire data per retention policy.

### Logging / Audit
- [ ] CloudTrail / Activity Log / Audit Log enabled, multi-region, log file validation on.
- [ ] Logs written to a separate account/project (blast-radius isolation).
- [ ] Alerting on root account use, IAM policy changes, security group changes.

### Secrets
- [ ] No secrets in env vars in Terraform `*.tf` files or Helm values.
- [ ] Secrets manager / vault references via data source, not literal strings.
- [ ] Rotation enabled where the provider supports it.

**Exit probe:** every item resolved Pass / Fail / N/A.

## Phase 4 — Container Checklist

### Dockerfile
- [ ] `FROM` pins to a digest (`@sha256:...`) or at least a specific tag — never `:latest`.
- [ ] Non-root `USER` set; `USER 0`/root only when documented and justified.
- [ ] `HEALTHCHECK` present.
- [ ] `COPY --chown=` used to avoid leaving root-owned files.
- [ ] No `ADD` with remote URL (use multi-stage + verified download).
- [ ] Minimal base image (distroless, alpine, scratch) — not full OS images for app containers.
- [ ] Multi-stage build to keep build tools out of final image.
- [ ] No build secrets in layers (use `--mount=type=secret`, not `ARG`).

### Runtime
- [ ] `--read-only` filesystem with explicit `tmpfs` mounts for writable paths.
- [ ] `--cap-drop=ALL` then `--cap-add` only needed caps.
- [ ] `--security-opt=no-new-privileges`.
- [ ] `seccomp` and `AppArmor` / SELinux profiles set (don't run with `unconfined`).

**Exit probe:** image scanned with Trivy or Grype; CRITICAL/HIGH triaged.

## Phase 5 — CI/CD Checklist

- [ ] Secrets stored in the platform's secret store, referenced by name. No `echo $SECRET` to logs.
- [ ] `pull_request` workflows do NOT have write access to the repo or secrets (GitHub Actions: `permissions: read-all` default, escalate per job).
- [ ] Third-party actions pinned to commit SHA, not tag (tag mutability risk).
- [ ] OIDC used for cloud auth (`aws-actions/configure-aws-credentials` with `role-to-assume`), not long-lived access keys.
- [ ] Branch protection on default branch: required reviews, required status checks, no force-push, signed commits if mandated.
- [ ] Required status checks include SAST + dependency audit.
- [ ] Artifact signing (cosign, Sigstore) for release builds.
- [ ] `workflow_dispatch` inputs validated; no shell injection via input interpolation into `run:`.

**Exit probe:** workflow files inspected; pinned-SHA check via `grep -E '@v[0-9]+' .github/workflows/*.yml` should return zero or be justified.

## Phase 6 — Kubernetes Checklist

### Pod Security
- [ ] Pod Security Admission (PSA) labels on namespaces: `restricted` for workloads, `baseline` minimum.
- [ ] `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`, `seccompProfile.type: RuntimeDefault`.
- [ ] No `hostNetwork`, `hostPID`, `hostIPC`, `privileged: true`.
- [ ] Resource requests + limits set (prevents resource-exhaustion DoS).

### Network
- [ ] `NetworkPolicy` resources: default-deny ingress + egress per namespace, then allow rules.
- [ ] No `LoadBalancer` services exposing internal-only workloads.
- [ ] Service mesh mTLS (Istio strict, Linkerd) where workload-to-workload sensitivity warrants it.

### RBAC
- [ ] No `cluster-admin` binding to ServiceAccounts other than break-glass.
- [ ] `Role` preferred over `ClusterRole` where namespace-scoped is enough.
- [ ] No wildcard verbs/resources in workload SAs.
- [ ] `automountServiceAccountToken: false` on pods that don't talk to the API.

### Secrets
- [ ] Sealed-Secrets / SOPS / External Secrets Operator — not plaintext `Secret` manifests in Git.
- [ ] etcd encryption at rest enabled (cluster-level).

**Exit probe:** PSA labels grep on namespace YAML; `runAsNonRoot` grep on Deployments/StatefulSets/DaemonSets.

## Phase 7 — Emit Findings

Per the output format in the parent `SKILL.md`. Findings reference the specific rule ID from the scanner that flagged them, plus CIS Controls v8.1 control number where applicable.

## Acceptance Criteria (workflow-level)

- All 7 phases completed; exit probes recorded.
- Scanner output files retained.
- Findings table emitted with all 7 fields per finding.
