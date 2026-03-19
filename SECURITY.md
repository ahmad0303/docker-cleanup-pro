# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Docker Cleanup Pro seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not:

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed

### Please Do:

**Report security vulnerabilities to: realahmad001@gmail.com** 

Please include the following information:

1. **Type of vulnerability** (e.g., privilege escalation, data exposure, injection)
2. **Full paths of affected source files** (if applicable)
3. **Location of the affected code** (tag/branch/commit or direct URL)
4. **Step-by-step instructions to reproduce the issue**
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact of the vulnerability** and potential attack scenarios
7. **Your contact information** for follow-up questions

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Updates**: We will send you regular updates about our progress
- **Timeline**: We aim to validate and address critical vulnerabilities within 30 days
- **Credit**: If you wish, we will publicly credit you for the discovery once the vulnerability is patched

### Security Update Process

1. Vulnerability is reported and acknowledged
2. Issue is verified and assessed for severity
3. Patch is developed and tested
4. Security advisory is prepared
5. Patch is released with security advisory
6. Public disclosure (after patch is available)

## Security Best Practices

When using Docker Cleanup Pro:

1. **Run with least privilege**: Only grant necessary Docker socket access
2. **Use dry-run first**: Always test with `--dry-run` before actual cleanup
3. **Review what will be removed**: Check the output before confirming
4. **Keep updated**: Use the latest version with security patches
5. **Limit access**: Restrict who can run cleanup operations
6. **Monitor logs**: Keep cleanup logs for audit trails
7. **Docker socket security**: 
   - Limit access to `/var/run/docker.sock`
   - Consider using Docker contexts for remote access
   - Run in containers with minimal permissions

## Known Security Considerations

### Docker Socket Access

Docker Cleanup Pro requires access to the Docker daemon socket. This is powerful and should be treated as root-equivalent access:

- Only run Docker Cleanup Pro with trusted code
- Be cautious when mounting `/var/run/docker.sock` in containers
- Consider using Docker's authorization plugins for additional security

### Container Cleanup

When cleaning containers:

- Running containers are never removed
- Check for data volumes before removing containers
- Ensure critical services won't be affected

## Dependency Security

We regularly update dependencies to address security vulnerabilities:

- Python Docker SDK is our primary dependency
- We use Dependabot for automated dependency updates
- Security patches are prioritized

## Vulnerability Disclosure Timeline

- **Day 0**: Vulnerability reported
- **Day 1-2**: Initial acknowledgment and triage
- **Day 3-7**: Vulnerability validation and severity assessment
- **Day 7-30**: Patch development and testing
- **Day 30**: Security release and public disclosure

## Security Hall of Fame

We recognize security researchers who help us keep Docker Cleanup Pro secure:
