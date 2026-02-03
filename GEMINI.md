# Gemini-Specific Instructions
> Optimizations and guidelines for Google AI Studio / Gemini models

This file supplements AGENTS.md with Gemini-specific capabilities and best practices.

## Gemini Model Selection

**For this CMS project, use:**
- **Gemini 1.5 Pro** - Best for complex orchestration, large codebases, architecture decisions
- **Gemini 1.5 Flash** - Fast iterations, code generation, simple tasks
- **Gemini 2.0 Flash** - Latest experimental features, fastest responses

**Current recommendation:** Gemini 1.5 Pro for reliability and context window (1M+ tokens)

## Leveraging Gemini's Strengths

### 1. Large Context Window (1M+ tokens)
You can load entire codebases into context:
- Load all directives at once
- Review full Laravel codebase
- Analyze Next.js component trees
- Compare multiple theme implementations

**Best practice:** When orchestrating complex tasks, load all relevant files first, then make decisions.

### 2. Native Code Execution
Gemini can execute Python directly. Use this for:
- Quick validation of execution scripts
- Testing API responses
- Data transformation previews
- Dry-run simulations

**Example workflow:**
```python
# Test API endpoint before generating full script
import requests
response = requests.get("https://api.example.com/products")
print(response.status_code, response.json()[:2])
```

### 3. Multimodal Capabilities
Gemini can analyze:
- **Screenshots:** UI/UX review, layout validation
- **Diagrams:** Database schemas, architecture flows
- **Design mockups:** Convert Figma/Sketch to Next.js components
- **Error screenshots:** Debug visual issues

**Use case:** User provides design mockup → You analyze it → Generate corresponding Next.js components with Tailwind CSS

### 4. Function Calling
Gemini excels at structured function calls. Define execution scripts as functions:

```python
# In your orchestration
def setup_laravel_backend(
    project_name: str,
    database_name: str,
    admin_panel: str = "filament"
) -> dict:
    """Set up Laravel backend with Docker"""
    # Implementation
    return {"status": "success", "container_id": "abc123"}
```

Then call them declaratively in your orchestration.

## Gemini-Optimized Workflows

### Directive Processing
1. **Load all directives** into context at session start
2. **Cross-reference** between directives to find dependencies
3. **Build execution graph** showing task order
4. **Validate prerequisites** before running scripts

### Error Recovery
Gemini's large context means you can:
- Keep full error logs in context
- Track error patterns across sessions
- Build error knowledge base
- Predict potential failures

### Code Generation
When generating Laravel or Next.js code:
1. **Review existing patterns** in codebase
2. **Follow established conventions** (PSR-12 for PHP, Airbnb for JS)
3. **Include tests** for new functionality
4. **Add JSDoc/PHPDoc** comments
5. **Validate against linters** before committing

## SEO Optimization with Gemini

### Automated SEO Audits
Use Gemini to:
- Analyze generated pages for SEO issues
- Validate structured data (JSON-LD)
- Check Core Web Vitals compliance
- Generate meta descriptions
- Create optimized alt texts for images

### Schema.org Generation
Gemini can generate complex JSON-LD schemas:

```typescript
// You can generate product schemas programmatically
const productSchema = {
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{{ product.name }}",
  "image": "{{ product.image }}",
  "description": "{{ product.description }}",
  "offers": {
    "@type": "Offer",
    "priceCurrency": "IDR",
    "price": "{{ product.price }}"
  }
}
```

Ask Gemini to generate schemas for each website type (Shop, Travel, Restaurant, Corporate).

## Docker Orchestration

### Container Health Checks
Generate health check scripts for `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Multi-stage Builds
Optimize Docker images with Gemini's help:
- Analyze dependencies
- Suggest caching layers
- Minimize image size
- Security scanning

## Gemini-Specific Directives

### Use Thinking Mode
For complex decisions (architecture, database design), use Gemini's extended thinking:
- Analyze trade-offs
- Consider edge cases
- Evaluate performance implications
- Recommend best approach with reasoning

### Batch Processing
Gemini can process multiple files simultaneously:
- Generate all migration files at once
- Create CRUD controllers for all models
- Build API resources for entire domain
- Generate test suites in parallel

## Language Considerations (Indonesia/Singapore)

### Localization Support
Gemini understands Indonesian context:
- Generate Indonesian translations
- Understand local payment methods (Midtrans, QRIS)
- Know local hosting providers
- Suggest Indonesia-specific SEO keywords

### Multi-language Content
For multi-language sites:
```php
// Laravel localization structure
resources/
  lang/
    en/
      messages.php
    id/
      messages.php
```

Gemini can generate translation files and maintain consistency.

## Performance Optimization

### Caching Strategies
Ask Gemini to analyze and suggest:
- Redis caching for API responses
- Next.js ISR (Incremental Static Regeneration)
- CDN integration (Cloudflare)
- Database query optimization

### Bundle Analysis
Gemini can review Next.js bundles:
- Identify large dependencies
- Suggest code splitting
- Recommend lazy loading
- Optimize images

## Security Best Practices

### Automated Security Review
Before deployment, ask Gemini to:
- Review `.env.example` for exposed secrets
- Check CORS configuration
- Validate input sanitization
- Audit SQL queries for injection risks
- Review authentication flow

### Dependency Scanning
Gemini can analyze `package.json` and `composer.json`:
- Flag outdated packages
- Identify security vulnerabilities
- Suggest alternatives
- Check license compatibility

## Testing Strategy

### Test Generation
Gemini excels at generating tests:

**Laravel (PHPUnit):**
```php
public function test_can_create_product()
{
    $response = $this->postJson('/api/v1/products', [
        'name' => 'Test Product',
        'price' => 100000
    ]);
    
    $response->assertStatus(201);
}
```

**Next.js (Jest + React Testing Library):**
```typescript
test('renders product card', () => {
  render(<ProductCard name="Test" price={100000} />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

## Deployment Automation

### CI/CD Pipeline Generation
Gemini can create GitHub Actions workflows:
- Run tests on pull requests
- Build Docker images
- Deploy to staging/production
- Run security scans

### Infrastructure as Code
Generate Terraform or Docker Swarm configs for Indonesian/Singapore hosting.

## Continuous Learning

### Session Memory
At the end of each session:
1. **Summarize learnings** (what worked, what failed)
2. **Update directives** with new insights
3. **Document edge cases** discovered
4. **Refine execution scripts** for better reliability

### Pattern Recognition
Gemini can identify recurring patterns:
- Common bugs in Laravel migrations
- Next.js hydration mismatches
- Docker networking issues
- SEO mistakes

Build a knowledge base in `docs/learnings/` for future reference.

## Best Practices Summary

✅ **Do:**
- Load full context before making decisions
- Use code execution for quick validation
- Generate comprehensive tests
- Leverage multimodal analysis for UI/UX
- Ask for extended thinking on complex architecture
- Keep error logs and patterns in context
- Generate localized content for Indonesian market

❌ **Don't:**
- Make assumptions about user's hosting environment
- Skip security validation
- Generate code without tests
- Ignore SEO requirements
- Forget to update directives after learning
- Hard-code credentials (always use `.env`)

## Gemini API Integration (Future)

If you integrate Gemini API into the CMS admin panel:
- Content generation for products/tours
- SEO meta description generation
- Image alt text automation
- Multi-language translation
- Chatbot for customer support

Store API keys securely in `.env`:
```env
GOOGLE_AI_API_KEY=your_gemini_api_key
GOOGLE_AI_MODEL=gemini-1.5-pro
```

---

**Remember:** Gemini's strength is intelligent orchestration with massive context. Use this to understand the entire system, make informed decisions, and continuously improve the CMS architecture.
