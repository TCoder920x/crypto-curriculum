# Documentation Directory

This directory contains all project documentation. **All documentation files should be placed here**, organized by category.

## 📁 Directory Structure

### `/api`
API documentation, endpoint specifications, and API usage guides.

**Examples:**
- API endpoint reference
- Request/response examples
- Authentication documentation
- API versioning guides

### `/deployment`
Deployment guides, infrastructure documentation, and operations procedures.

**Examples:**
- Deployment checklists
- Environment setup guides
- Server configuration
- Docker/Kubernetes configs documentation
- CI/CD pipeline documentation

### `/architecture`
System architecture diagrams, technical design documents, and infrastructure documentation.

**Examples:**
- System architecture diagrams
- Database schema diagrams
- Data flow diagrams
- Component interaction diagrams
- Technology stack decisions

### `/guides`
User guides, developer guides, and how-to documentation.

**Examples:**
- Developer onboarding guides
- Code contribution guidelines
- Style guides
- Testing guides
- Troubleshooting guides

## 📝 Documentation Guidelines

### File Naming
- Use lowercase with hyphens: `api-authentication.md`
- Be descriptive: `deployment-production-checklist.md`
- Include version if needed: `api-v1-reference.md`

### Format
- **Primary format**: Markdown (.md)
- **Diagrams**: Use Mermaid, PlantUML, or include as images
- **API specs**: OpenAPI/Swagger YAML or JSON

### What Goes Here vs. README Files

| Documentation Type | Location |
|-------------------|----------|
| **Project overview** | Root `README.md` |
| **Component-specific setup** | Component's `README.md` (e.g., `app/frontend/README.md`) |
| **General architecture** | `docs/architecture/` |
| **API documentation** | `docs/api/` |
| **Deployment procedures** | `docs/deployment/` |
| **Comprehensive guides** | `docs/guides/` |
| **Code examples** | `curriculum/code-examples/` (for teaching) |

## 🎯 Best Practices

1. **Keep documentation updated** - Update docs when code changes
2. **Use clear headings** - Make content scannable
3. **Include examples** - Show, don't just tell
4. **Link between docs** - Create a connected documentation web
5. **Version important docs** - Track major documentation changes
6. **Use diagrams** - A picture is worth a thousand words

## 📚 Recommended Documentation

### Essential (Create These First)
- [ ] API endpoint reference (`api/endpoints.md`)
- [ ] Deployment guide (`deployment/getting-started.md`)
- [ ] Architecture overview (`architecture/system-overview.md`)
- [ ] Developer setup guide (`guides/developer-setup.md`)

### Nice to Have
- [ ] Database schema documentation (`architecture/database-schema.md`)
- [ ] Authentication flow diagram (`architecture/auth-flow.md`)
- [ ] Production deployment checklist (`deployment/production-checklist.md`)
- [ ] Testing guide (`guides/testing.md`)
- [ ] Code style guide (`guides/style-guide.md`)

---

**Remember:** READMEs can stay in their relevant component directories, but comprehensive documentation belongs here in `/docs`.

