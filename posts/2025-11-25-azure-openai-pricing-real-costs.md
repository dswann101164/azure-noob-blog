---
title: "Azure OpenAI Real Costs 2026: PTU vs Pay-As-You-Go Calculator"
date: 2025-11-25
modified: 2026-01-02
summary: "Microsoft's calculator shows $150/mo. You'll actually pay $1,906. Free break-even calculator shows when to switch to PTU. No consultant required."
tags:
- Azure
- FinOps
- AI
- OpenAI
- Cost Management
cover: /static/images/hero/azure-openai-costs.png
slug: azure-openai-pricing-real-costs
hub: finops
related_posts:
  - azure-finops-complete-guide
  - azure-cost-optimization-complete-guide
  - azure-resource-tags-guide
faq_schema: true
---

<div style="background: #f8f9fa; padding: 2rem; border-left: 4px solid #0078d4; margin: 2rem 0; border-radius: 4px;">
  <h2 style="margin-top: 0; color: #0078d4;">⚡ Quick Answer: Azure OpenAI Pricing 2026</h2>
  <p style="font-size: 1.1rem; margin-bottom: 1rem;">
    <strong>GPT-4o:</strong> $0.005 per 1K input tokens, $0.015 per 1K output tokens<br>
    <strong>GPT-4o mini:</strong> $0.00015 per 1K input tokens, $0.0006 per 1K output tokens<br>
    <strong>PTU (Provisioned Throughput):</strong> Starting at $2,448/month
  </p>
  <p style="margin-bottom: 0;"><strong>Hidden Costs:</strong> Fine-tuning hosting adds $1,836-2,160/month per model. Infrastructure overhead adds $35-50/month. A $4 calculator estimate becomes $1,906 in production.</p>
</div>

<div style="text-align: center; margin: 2.5rem 0; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px;">
  <h3 style="color: white; margin-top: 0; font-size: 1.75rem;">💰 Calculate Your Real Azure OpenAI Costs</h3>
  <p style="color: white; font-size: 1.1rem; margin-bottom: 1.5rem;">
    Get the <strong>2026 Azure OpenAI ROI & Cost Optimization Toolkit ($497)</strong><br>
    <span style="font-size: 0.95rem; opacity: 0.9;">Interactive Excel calculator • TCO models • PTU analysis • No consulting needed</span>
  </p>
  <a href="https://davidnoob.gumroad.com/l/azure-openai-roi-toolkit" 
     style="display: inline-block; padding: 1rem 2.5rem; background: white; color: #667eea; text-decoration: none; border-radius: 6px; font-weight: 700; font-size: 1.15rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: all 0.3s ease;"
     target="_blank" rel="noopener">
    Get the ROI Toolkit →
  </a>
  <p style="color: white; margin: 1rem 0 0; font-size: 0.9rem; opacity: 0.9;">
    Tested on 30,000+ Azure resources • Instant digital delivery
  </p>
</div>

## Azure OpenAI Pricing 2026: Complete Price Reference

Here are the current token costs for the most commonly used models (January 2026):

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Best For |
|-------|----------------------|------------------------|----------|
| **GPT-4o** | $0.005 | $0.015 | General production use, best price/performance |
| **GPT-4o mini** | $0.00015 | $0.0006 | High-volume simple tasks, 60× cheaper |
| **GPT-4 Turbo** | $0.01 | $0.02 | Complex reasoning, code generation |
| **GPT-4 (32K)** | $0.06 | $0.12 | Large context windows (rarely needed) |
| **GPT-3.5 Turbo** | $0.002 | $0.002 | Simple tasks, legacy compatibility |

**Hidden costs not in the table:**
- Fine-tuned model hosting: **$1,836-$2,160/month** per model (flat fee)
- Infrastructure overhead: **$35-50/month** (Cognitive Services, Key Vault, monitoring)
- Output tokens cost **2× more** than input tokens
- PTU (Provisioned Throughput): Starting at **$2,448/month** (enterprise only)

**Example real cost:** A "$4/month" calculator estimate becomes **$1,906/month** in production when fine-tuning and infrastructure are included.

---

## What does Azure OpenAI actually cost?

**Short Answer:** Azure OpenAI runs $0.002-$0.06 per 1,000 tokens depending on model (GPT-3.5 to GPT-4), but production deployments cost 10×-50× more than Microsoft's calculator shows. The calculator omits fine-tuning hosting fees ($1,836-$2,160/month per model regardless of usage), infrastructure requirements (Cognitive Services resources, Key Vault, monitoring adding $35-50/month), and the 2× cost multiplier for output tokens versus input tokens. A $4/month calculator estimate becomes $1,900+/month when fine-tuning deploys to production.

---

📊 **Free Download: Azure OpenAI Cost Calculator**

Calculate your REAL production costs (not what Microsoft's calculator shows). Professional Excel workbook with:
- **Interactive cost calculator** with live formulas
- **Model comparison** (GPT-3.5 vs GPT-4 vs GPT-4o)
- **5 cost optimization strategies** proven to reduce spend by 60%
- **Real production example** ($4 estimate → $1,906 actual bill)
- **ROI analysis** for model selection decisions

**[Download Calculator (Excel)](/static/downloads/Azure_OpenAI_Cost_Calculator.xlsx)** | **[Subscribe for Azure FinOps updates](https://azure-noob.com)**

*No email required for download. Created by David Swann, Azure Architect.*

---

### Why Microsoft's pricing calculator is always wrong

Microsoft's [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) shows token costs only. It assumes:
- Pay-as-you-go token pricing with no fine-tuning
- Zero infrastructure costs beyond the API
- Equal input/output token ratios (actual: output tokens cost 2× more)
- No hosting fees, monitoring, or supporting services

These assumptions never match production deployments.

---

<div style="background: linear-gradient(135deg, #e3f2fd 0%, #fff 100%); border-left: 4px solid #0078d4; padding: 2rem; margin: 2rem 0; border-radius: 8px;">
  <h3 style="margin: 0 0 0.5rem 0; color: #0078d4; font-size: 1.5rem;">🎯 FREE: Azure OpenAI Break-Even Calculator (Lite)</h3>
  <p style="margin: 0 0 1rem 0; font-size: 1.05rem;"><strong>Stop guessing when to switch to PTU.</strong> Get our free Excel calculator that shows:</p>
  <ul style="margin: 0 0 1.5rem 0; padding-left: 1.5rem;">
    <li>Your current pay-as-you-go cost (actual, not Microsoft's estimate)</li>
    <li>PTU cost with 1-year and 3-year commitment pricing</li>
    <li>Monthly break-even point (the day PTU becomes cheaper)</li>
  </ul>
  <p style="margin: 0 0 1rem 0; font-size: 0.95rem; font-weight: 600;">Used by 200+ enterprise architects to justify $500K+ Azure budgets.</p>
  <form action="https://app.convertkit.com/forms/8896829/subscriptions" method="post" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
    <input type="email" name="email_address" placeholder="Enter your email" required style="flex: 1; min-width: 250px; padding: 0.875rem; border: 2px solid #ddd; border-radius: 6px; font-size: 1rem;">
    <button type="submit" style="padding: 0.875rem 2rem; background: #0078d4; color: white; border: none; border-radius: 6px; font-weight: 700; font-size: 1rem; cursor: pointer;">Send Me The Calculator →</button>
  </form>
  <p style="margin: 1rem 0 0; font-size: 0.85rem; opacity: 0.8;">Used by 200+ enterprise architects. No spam, unsubscribe anytime.</p>
  <p style="margin: 0.5rem 0 0; font-size: 0.9rem;"><em>Want the full ROI toolkit with TCO models, optimization strategies, and CFO-ready reports? <a href="/blog/openai-toolkit/" style="color: #0078d4; font-weight: 600;">See Enterprise Edition ($497) →</a></em></p>
</div>

---

### What breaks between calculator and production

**Calculator shows:** 1M input tokens + 1M output tokens with GPT-3.5 = $4/month

**Production reality adds:**
- Fine-tuned model hosting: $1,836/month (even if unused)
- Infrastructure overhead: $35/month (Cognitive Services, Key Vault, monitoring)
- Output token premium: 2× input token cost
- Retry/error overhead: 10-15% additional usage
- **Actual total: $1,906/month**

The gap: **47,000%**

---

## December 2025 Pricing Update

**What changed in late 2025:**
- GPT-4 Turbo: $0.01/1K input tokens (down from $0.03)
- GPT-4o (new): $0.005/1K input tokens (cheapest GPT-4-class model)
- PTU (Provisioned Throughput): $2,448/month minimum (up from $1,224)
- Fine-tuning hosting: $1,836/month minimum (up from $1,224)

**This guide reflects current December 2025 pricing with production deployment experience across enterprise Azure environments.**

---

**Azure OpenAI pricing looks simple until you get your first bill.**

Microsoft's pricing calculator shows you: "GPT-4: $0.01 per 1,000 input tokens, $0.02 per 1,000 output tokens." Clean. Straightforward. Wrong.

Because that calculator doesn't tell you about:
- The fine-tuned model hosting fee ($1,836/month minimum, whether you use it or not)
- The PTU (Provisioned Throughput Units) pricing that could save you 70% but requires enterprise agreements
- The infrastructure costs beyond the API (Cognitive Services resources, storage, monitoring)
- The fact that GPT-4 output tokens cost **2x more than input tokens** and nobody explains token ratio impact

I spent $500 testing Azure OpenAI deployments across development and production environments in a large enterprise Azure setup. Here's what the pricing calculator won't tell you.

This is part of our complete [Azure FinOps implementation guide](/blog/azure-finops-complete-guide/) covering cost visibility, chargeback models, and tag governance for enterprise Azure environments. [Azure OpenAI](/blog/azure-openai-pricing-real-costs/) cost management requires the same foundational FinOps practices as any other Azure service.

## What Microsoft's Calculator Shows You

Go to the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) and add "Azure OpenAI Service."

You'll see:
- Model selection (GPT-3.5, GPT-4, GPT-4o, etc.)
- Token count inputs
- Monthly cost estimate

**Example from the calculator:**
- 1 million input tokens
- 1 million output tokens  
- GPT-3.5-Turbo model
- **Estimated cost: $4/month**

Looks affordable, right?

## Why does Azure OpenAI pricing look cheap in the calculator but expensive in production?

**Cause:** The Azure pricing calculator only models API token usage and ignores required infrastructure, hosting fees, and non-token service costs.

**Effect:** Real-world Azure OpenAI deployments routinely cost 10×–100× more than calculator estimates once production traffic, fine-tuning, and supporting services are included.

**What to do:** Model total cost using real traffic volumes, include all dependent Azure services, and validate pricing with a controlled pilot before scaling workloads.

**My actual first month costs:**
- API token usage (as estimated): $47
- Cognitive Services resource (required infrastructure): $12
- Fine-tuned model hosting (deployed but inactive): $1,836
- Azure Monitor logs and diagnostics: $8
- Key Vault for API key management: $3
- **Total: $1,906**

The calculator said $4. The bill said $1,906.

**What went wrong?** Everything Microsoft doesn't tell you about.

## What hidden costs does Azure OpenAI pricing not show upfront?

> **The Ownership Gap (Why you will go over budget)**
> 
> You can calculate token costs all day `(technical problem)`, but if no one signs off on the budget `(governance problem)`, you're just monitoring a cash fire. This is the **Implementation Gap**. 
> 
> Most engineers deploy the model first and ask "Who pays for this?" later. That delay costs $2,000/month in hosting fees while you argue over cost centers. You need to define ownership *before* deployment.


### 1. Fine-Tuned Model Hosting Fees

If you deploy a fine-tuned model, Azure charges you **$2.52-$3.00 per hour** just to keep it running.

That's **$1,836 to $2,160 per month** for hosting, regardless of whether you send it a single request.

From Microsoft's own documentation:
> "The hosting hours cost is important to be aware of because after a fine-tuned model is deployed, it continues to incur an hourly cost regardless of whether you're actively using it."

---

## 💸 Calculate Your Real Azure OpenAI Costs (Before the CFO Does)

<div style="background: #f8f9fa; padding: 30px; border-radius: 8px; border-left: 5px solid #dc3545; margin: 30px 0;">

<h3 style="margin-top: 0; color: #dc3545;">⚠️ The Reality Check Calculator</h3>

<p style="font-size: 1.1em; margin-bottom: 25px;">Microsoft's calculator shows token costs. This shows what you actually pay.</p>

<div style="background: white; padding: 25px; border-radius: 6px; margin-bottom: 20px;">

<div style="margin-bottom: 20px;">
  <label style="display: block; font-weight: bold; margin-bottom: 8px;">Monthly Requests:</label>
  <input type="number" id="monthlyRequests" value="100000" style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;" />
</div>

<div style="margin-bottom: 20px;">
  <label style="display: block; font-weight: bold; margin-bottom: 8px;">Average Input Tokens per Request:</label>
  <input type="number" id="inputTokens" value="100" style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;" />
</div>

<div style="margin-bottom: 20px;">
  <label style="display: block; font-weight: bold; margin-bottom: 8px;">Average Output Tokens per Request:</label>
  <input type="number" id="outputTokens" value="300" style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;" />
</div>

<div style="margin-bottom: 20px;">
  <label style="display: block; font-weight: bold; margin-bottom: 8px;">Model:</label>
  <select id="modelType" style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;">
    <option value="gpt35">GPT-3.5 Turbo</option>
    <option value="gpt4o">GPT-4o</option>
    <option value="gpt4turbo" selected>GPT-4 Turbo</option>
    <option value="gpt4">GPT-4 (32K)</option>
  </select>
</div>

<div style="margin-bottom: 20px;">
  <label style="display: block; font-weight: bold; margin-bottom: 8px;">Fine-Tuned Models Deployed:</label>
  <input type="number" id="fineTunedModels" value="0" style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;" />
</div>

<button onclick="calculateCosts()" style="width: 100%; padding: 15px; background: #dc3545; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px;">Calculate Real Costs</button>

</div>

<div id="results" style="display: none; background: white; padding: 25px; border-radius: 6px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">

<div style="text-align: center; padding: 20px; background: #e7f3ff; border-radius: 6px;">
  <div style="font-size: 14px; color: #666; margin-bottom: 8px;">Microsoft's Calculator Says:</div>
  <div id="calculatorCost" style="font-size: 32px; font-weight: bold; color: #0078d4;">$0</div>
  <div style="font-size: 12px; color: #666; margin-top: 5px;">Token costs only</div>
</div>

<div style="text-align: center; padding: 20px; background: #ffe7e7; border-radius: 6px;">
  <div style="font-size: 14px; color: #666; margin-bottom: 8px;">You Actually Pay:</div>
  <div id="actualCost" style="font-size: 32px; font-weight: bold; color: #dc3545;">$0</div>
  <div style="font-size: 12px; color: #666; margin-top: 5px;">Full production cost</div>
</div>

</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 6px; border-left: 4px solid #ffc107; margin-bottom: 20px;">
  <div style="font-weight: bold; margin-bottom: 10px;">💰 The Hidden Costs:</div>
  <div id="breakdown"></div>
</div>

<div id="gap" style="text-align: center; padding: 20px; background: #dc3545; color: white; border-radius: 6px; font-size: 20px; font-weight: bold;"></div>

</div>

</div>

<script>
function calculateCosts() {
  const requests = parseInt(document.getElementById('monthlyRequests').value) || 0;
  const inputTokens = parseInt(document.getElementById('inputTokens').value) || 0;
  const outputTokens = parseInt(document.getElementById('outputTokens').value) || 0;
  const model = document.getElementById('modelType').value;
  const fineTuned = parseInt(document.getElementById('fineTunedModels').value) || 0;

  // Token pricing per 1K tokens
  const pricing = {
    gpt35: { input: 0.002, output: 0.002 },
    gpt4o: { input: 0.005, output: 0.015 },
    gpt4turbo: { input: 0.01, output: 0.02 },
    gpt4: { input: 0.06, output: 0.12 }
  };

  const prices = pricing[model];

  // Token costs
  const totalInputTokens = requests * inputTokens;
  const totalOutputTokens = requests * outputTokens;
  const tokenCost = ((totalInputTokens / 1000) * prices.input) + ((totalOutputTokens / 1000) * prices.output);

  // Hidden costs
  const fineTunedCost = fineTuned * 1836; // $1,836/month per model
  const infrastructureCost = 35; // Cognitive Services, Key Vault, monitoring
  const retryOverhead = tokenCost * 0.10; // 10% retry overhead

  const calculatorEstimate = tokenCost;
  const actualTotal = tokenCost + fineTunedCost + infrastructureCost + retryOverhead;

  // Display results
  document.getElementById('calculatorCost').textContent = '$' + Math.round(calculatorEstimate).toLocaleString();
  document.getElementById('actualCost').textContent = '$' + Math.round(actualTotal).toLocaleString();

  const gapPercent = Math.round(((actualTotal - calculatorEstimate) / calculatorEstimate) * 100);
  document.getElementById('gap').textContent = 'The Gap: ' + gapPercent.toLocaleString() + '%';

  const breakdown = `
    <div style="margin-bottom: 8px;">• Token Costs: $${Math.round(tokenCost).toLocaleString()}</div>
    ${fineTuned > 0 ? `<div style="margin-bottom: 8px;">• Fine-Tuned Model Hosting: $${Math.round(fineTunedCost).toLocaleString()} (${fineTuned} model${fineTuned > 1 ? 's' : ''})</div>` : ''}
    <div style="margin-bottom: 8px;">• Infrastructure Overhead: $${infrastructureCost}</div>
    <div style="margin-bottom: 8px;">• Error Retry Overhead: $${Math.round(retryOverhead).toLocaleString()}</div>
  `;

  document.getElementById('breakdown').innerHTML = breakdown;
  document.getElementById('results').style.display = 'block';
}
</script>

---

**The kicker:** If your fine-tuned model sits inactive for 15 days, Azure auto-deletes it. But if you use it even once during those 15 days, the billing clock keeps running.

**Real-world impact:**
- Development environment with fine-tuned GPT-3.5: $1,836/month minimum
- Production environment with fine-tuned GPT-4: $2,160/month minimum
- Total hosting before processing a single token: $3,996/month

The pricing calculator? Doesn't mention this at all.

---

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 12px; color: white; margin: 60px 0; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);">

<h2 style="color: white; margin-top: 0; font-size: 2.2rem; text-align: center;">🎯 Stop the Bleed: Azure AI FinOps Query Pack ($19)</h2>

<p style="text-align: center; font-size: 1.3rem; margin-bottom: 30px; font-weight: bold;">One query just saved you $1,836/month. That's 97× what this pack costs.</p>

<div style="background: rgba(255, 255, 255, 0.15); padding: 30px; border-radius: 8px; margin: 20px 0;">

<h3 style="color: white; margin-top: 0; font-size: 1.6rem;">What's Inside (12 Production-Tested KQL Queries)</h3>

<div style="margin: 20px 0; line-height: 2;">
<p style="margin: 10px 0;">✅ <strong>Find Zombie Fine-Tuned Models</strong> → $1,836/month waste per model</p>
<p style="margin: 10px 0;">✅ <strong>Calculate Chargeback by Application Tag</strong> → CFO-approved accuracy</p>
<p style="margin: 10px 0;">✅ <strong>Detect Output-to-Input Ratio Outliers</strong> → 62% cost reduction opportunity</p>
<p style="margin: 10px 0;">✅ <strong>Track AI Spend Across 40+ Subscriptions</strong> → Enterprise visibility</p>
<p style="margin: 10px 0;">✅ <strong>Identify Error Rate Overhead</strong> → Find 15% waste from retries</p>
<p style="margin: 10px 0;">✅ <strong>Fine-Tuning ROI Calculator</strong> → Justify the $1,836 fee... or kill it</p>
</div>

<h3 style="color: white; margin-top: 30px; font-size: 1.6rem;">Why Trust This Code?</h3>

<p style="margin: 15px 0; font-size: 1.1rem;"><strong>These queries are production-tested, not tutorial-tested.</strong></p>

<p style="margin: 10px 0;">Built to handle enterprise-scale infrastructure:</p>
<ul style="margin: 10px 0 10px 20px; line-height: 1.8;">
<li>30,000+ resources across 40+ subscriptions</li>
<li>Complex tag schemas with semantic inconsistencies</li>
<li>Multi-domain Active Directory environments</li>
<li>FinOps requirements where executives demand answers</li>
</ul>

<p style="margin: 20px 0 10px 0;"><strong>The Reality:</strong></p>
<p style="margin: 10px 0;">Consultants charge $5K for an assessment that tells you "you have zombie resources." This pack gives you the EXACT query that finds them, costs $19, and runs in 30 seconds.</p>

<p style="margin: 10px 0;">These queries were built debugging real production incidents—like finding 4 forgotten fine-tuned models bleeding $7,344/month from dev subscriptions. One query found all four. Deleted them that day.</p>

<p style="margin: 20px 0 10px 0;"><strong>What customers are finding:</strong></p>
<ul style="margin: 10px 0 10px 20px; line-height: 1.8;">
<li>Healthcare system: 4 idle models = $7,344/month waste (found in 3 minutes)</li>
<li>Financial services: 12:1 output ratio chatbot = $5,200/month excess (fixed with max_tokens: 150)</li>
<li>Tech company: $12,400/month untagged AI resources (now allocated correctly)</li>
</ul>

<h3 style="color: white; margin-top: 30px; font-size: 1.6rem;">What You Get</h3>

<div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 6px; margin: 15px 0;">
<p style="margin: 8px 0;">📦 <strong>12 Copy-Paste KQL Queries</strong> — Enterprise-scale tested on 31,000+ resources</p>
<p style="margin: 8px 0;">📊 <strong>Real-World Examples</strong> — Actual savings from enterprise production environments</p>
<p style="margin: 8px 0;">🔄 <strong>Lifetime Updates</strong> — New queries as Azure pricing changes, GPT-5 included</p>
<p style="margin: 8px 0;">💯 <strong>Money-Back Guarantee</strong> — If ONE query doesn't save you $100, instant refund</p>
</div>

</div>

<div style="text-align: center; margin: 30px 0;">
<a href="https://davidnoob.gumroad.com/l/syvej?ref=pricing-post-calculator" style="display: inline-block; background: #ff6b35; color: white; padding: 20px 50px; border-radius: 8px; text-decoration: none; font-size: 1.3em; font-weight: bold; box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4); transition: all 0.3s;">🔥 Get Query Pack - $19 (Launch Price)</a>
</div>

<div style="text-align: center; font-size: 0.95em; opacity: 0.9;">
<p><strong>⏰ Launch price ends January 31, 2026</strong></p>
<p>Regular price: $29 | Launch: $19 (save $10)</p>
<p>📦 Instant download | 📧 No email required | 🔒 Secure checkout</p>
</div>

<h3 style="color: white; margin-top: 40px; font-size: 1.5rem;">The Alternative</h3>

<p style="margin: 15px 0;">Keep using the Azure Portal's basic cost reports. Spend 10 hours manually correlating Cost Management exports with Resource Graph data every time the CFO asks "where's our AI money going?"</p>

<p style="margin: 15px 0;">Or run Query #2 and get a perfect chargeback report in 30 seconds.</p>

<p style="margin: 15px 0; font-weight: bold; font-size: 1.2rem;">Your choice.</p>

</div>

---

### 2. Input vs Output Token Pricing (The 2x Multiplier)

Microsoft's calculator shows token costs. What it doesn't emphasize: **output tokens cost 2x more than input tokens.**

**GPT-4 Turbo pricing breakdown (Dec 2025):**
- Input tokens: $0.01 per 1,000 tokens
- Output tokens: $0.02 per 1,000 tokens

**Why this matters:**

Let's say you're building a customer support chatbot. Each interaction:
- Customer question: 100 tokens (input)
- AI response: 400 tokens (output)
- **Total tokens: 500**

**But the cost isn't equal:**
- Input cost: (100 / 1,000) × $0.01 = $0.001
- Output cost: (400 / 1,000) × $0.02 = $0.008
- **Total: $0.009 per interaction**

If your AI generates verbose responses (and GPT-4 loves to be thorough), **89% of your cost is output tokens.**

Run 10,000 support interactions per month:
- Calculator estimate (assuming equal token cost): ~$75
- Actual cost (accounting for 4:1 output ratio): $90

**The calculator assumes you know this. Most people don't.**

### 3. GPT-4 vs GPT-3.5 vs GPT-4o Cost Comparison

Microsoft offers multiple models. The calculator lets you switch between them. What it doesn't tell you: **the cost differences are massive.**

**Token pricing comparison (December 2025):**

| Model | Input (per 1K) | Output (per 1K) | Cost vs GPT-3.5 |
|-------|----------------|-----------------|-----------------|
| GPT-3.5-Turbo | $0.002 | $0.002 | 1x (baseline) |
| GPT-4o | $0.005 | $0.015 | 4x |
| GPT-4 Turbo | $0.01 | $0.02 | 7.5x |
| GPT-4 (32K) | $0.06 | $0.12 | 45x |

**Real example:**

Converting a 1,000-token JavaScript code sample to Python:
- Input: 1,000 tokens (the code sample)
- Output: 1,000 tokens (the Python version)

**GPT-3.5 cost:**
- (1,000 / 1,000 × $0.002) + (1,000 / 1,000 × $0.002) = **$0.004**

**GPT-4o cost:**
- (1,000 / 1,000 × $0.005) + (1,000 / 1,000 × $0.015) = **$0.02**

**GPT-4 Turbo cost:**
- (1,000 / 1,000 × $0.01) + (1,000 / 1,000 × $0.02) = **$0.03**

Same task. GPT-4 Turbo is **7.5x more expensive** than GPT-3.5.

**When is GPT-4 worth it?**

After testing models in production:

✅ **Use GPT-4 Turbo for:**
- Complex analysis requiring reasoning (security assessments, code reviews)
- High-stakes content where accuracy matters (legal documents, financial reports)
- Tasks where a mistake costs more than the API call (compliance checks)

✅ **Use GPT-4o for:**
- Balance of quality and cost (4x GPT-3.5, but better quality)
- General-purpose applications
- Mixed workloads with varying complexity

❌ **Use GPT-3.5 for:**
- Simple summarization
- Formatting and data transformation
- Basic customer support
- High-volume, low-complexity tasks

**The rule:** If you can't justify why GPT-4's quality improvement is worth 7.5x the cost, use GPT-4o or GPT-3.5.

### 4. PTU Pricing: The Enterprise Option Nobody Explains

Microsoft offers two pricing models:

1. **Pay-as-you-go** (what the calculator shows)
2. **PTU (Provisioned Throughput Units)** - what enterprises actually use

**PTU pricing (December 2025):**
- Reserve processing capacity (measured in PTUs)
- Starting at $2,448/month per PTU
- Pay monthly or annually
- Save up to 70% compared to pay-as-you-go on high-volume workloads
- Requires capacity planning and enterprise agreements

**The problem:** The pricing calculator doesn't show PTU costs.

**How PTUs work:**

Instead of paying per token, you pay for reserved capacity:
- 1 PTU = guaranteed processing throughput
- Pricing: $2,448-$3,600 per PTU per month (varies by region)
- Enterprise reservations (annual) get 50-70% discounts

**When PTUs make sense:**

We calculated the breakpoint:
- Pay-as-you-go: ~$5,000/month for production chatbot workload
- PTU with annual reservation: $1,800/month (64% savings)

**But** - you need to:
- Predict your usage accurately (you're paying regardless)
- Commit to annual contracts
- Work with Microsoft sales (no self-service)

The calculator won't help you here. You need actual usage data and a sales conversation.

### 5. Infrastructure Costs Beyond the API

Azure OpenAI doesn't run in isolation. You need:

**Required resources:**
- **Azure Cognitive Services resource** (container for OpenAI): $0-$12/month depending on tier
- **Key Vault** (API key management): ~$3/month with monitoring
- **Virtual Network** (if using private endpoints): $0.01/hour per endpoint = $7.20/month
- **Storage Account** (for fine-tuning data, logs): $2-5/month
- **Azure Monitor** (logging and diagnostics): $5-50/month depending on volume

**Example production setup costs:**
- API token usage: $500/month
- Infrastructure overhead: $35/month
- **Total: $535/month**

The calculator shows $500. You pay $535.

Not huge. But multiply by 10 production workloads and suddenly you're $350/month over budget.

These infrastructure costs exemplify why [Azure costs should be tracked by application, not subscription](/blog/azure-costs-apps-not-subscriptions/). Azure Cost Management reports won't automatically connect your Cognitive Services costs to your business applications without proper tagging.

## The Real Cost Calculator Nobody Gives You

Here's the formula I actually use:

```
Total Monthly Cost = 
  (Token Usage Cost) +
  (Fine-tuned Model Hosting × Models × 730 hours) +
  (Infrastructure Overhead) +
  (Hidden usage from retries, errors, testing)
```

**Example calculation for a production chatbot (December 2025 pricing):**

```
Token usage:
- 1M interactions/month
- Average 100 input + 300 output tokens per interaction
- Using GPT-4 Turbo

Input cost: 
  1M × 100 / 1,000 × $0.01 = $1,000

Output cost:
  1M × 300 / 1,000 × $0.02 = $6,000

Fine-tuning hosting:
  1 model × $2.52/hour × 730 hours = $1,840

Infrastructure:
  Cognitive Services + Storage + Monitoring = $35

Error retry overhead (10%):
  ($1,000 + $6,000) × 0.10 = $700

Total: $9,575/month
```

**Microsoft's calculator estimate for the same workload: $7,000**

The difference: $2,575/month = $30,900/year.

## What I Learned Deploying This at Scale

**1. Start with GPT-3.5, prove value, then upgrade**

Don't start with GPT-4 because it's "better." Start with GPT-3.5, measure quality, and upgrade specific use cases that need it.

We saved $15,000/month by running 80% of workloads on GPT-3.5 and reserving GPT-4 for complex analysis.

**2. Never deploy a fine-tuned model without a deletion schedule**

If you're testing fine-tuning, deploy it, test it, and **immediately delete it** if you're not using it actively.

We had three fine-tuned models running in dev environments that nobody was using. Cost: $5,508/month (at current rates).

**3. Monitor token usage per endpoint, not per subscription**

Azure Cost Management shows [OpenAI costs](/blog/azure-openai-pricing-real-costs/) at the subscription level. That's useless.

Tag every deployment with `Application` and `Environment` tags. Query costs using Resource Graph:

```kusto
Resources
| where type == "microsoft.cognitiveservices/accounts"
| where kind == "OpenAI"
| extend appName = tostring(tags['Application'])
| join kind=inner (
    consumptionusage
    | where ResourceType == "microsoft.cognitiveservices/accounts"
    | summarize Cost = sum(PreTaxCost) by ResourceId
) on $left.id == $right.ResourceId
| project appName, Cost
| order by Cost desc
```

This shows cost per application. Critical for chargeback.

For a complete chargeback implementation strategy, see our guide on [Azure chargeback models](/blog/azure-chargeback-tags-model/) that business units actually accept, including hybrid allocation models and shared services costs.

**4. Use PTUs for production, pay-as-you-go for dev**

Development and testing workloads are unpredictable. Use pay-as-you-go.

Production workloads with steady traffic? Switch to PTUs and get 50-70% savings with annual reservations.

**5. Input token optimization saves more than output optimization**

Everyone focuses on making AI responses shorter. Wrong approach.

**Better:** Make prompts more efficient.

We reduced our average prompt from 800 tokens to 300 tokens by:
- Removing unnecessary context
- Using function calling instead of verbose instructions  
- Pre-processing inputs before sending to the API

**Savings:** 62% reduction in input costs.

## When Does Azure OpenAI Actually Save Money Compared to On-Premises AI?

Azure OpenAI becomes cost-effective when token volume exceeds 50M tokens/month but remains below the PTU breakpoint where provisioned capacity makes sense. Organizations processing 10-30M tokens/month pay $200-600 using pay-as-you-go pricing, while equivalent on-premises GPU infrastructure (NVIDIA A100 instances) costs $8,000-$15,000/month in hardware amortization, power, and maintenance.

The crossover point is approximately 100M tokens/month, where Azure costs reach $2,000-$3,000 and provisioned capacity (PTU) reduces this to $2,448/month with annual commitment. Below 10M tokens/month, Azure is definitively cheaper. Above 200M tokens/month, on-premises infrastructure with equivalent GPUs becomes cost-competitive if you can manage the operational complexity.

**Real breakpoint analysis:**

**10M tokens/month scenario:**
- Azure OpenAI (GPT-4 Turbo): $150/month
- On-premises GPU cluster: $12,000/month (hardware, power, engineering)
- **Winner: Azure by $11,850/month**

**100M tokens/month scenario:**
- Azure OpenAI pay-as-you-go: $3,000/month
- Azure OpenAI with PTU: $2,448/month (annual commit)
- On-premises GPU cluster: $8,000/month (amortized)
- **Winner: Azure PTU by $5,552/month**

**500M tokens/month scenario:**
- Azure OpenAI pay-as-you-go: $15,000/month
- Azure OpenAI with PTU: $7,344/month (3 PTUs)
- On-premises GPU cluster: $6,500/month (amortized at scale)
- **Winner: Competitive, depends on operational capability**

The decision isn't purely financial. On-premises requires:
- 2-3 FTE ML engineers ($300K-$450K/year)
- Data center space and cooling
- Hardware refresh cycles (3-4 years)
- Model updates and maintenance
- Compliance and security overhead

Azure OpenAI makes sense for most enterprises until you're processing 500M+ tokens/month consistently AND have the ML engineering team to run infrastructure.

## How Do You Calculate Actual Token Usage Before Deployment?

Calculate realistic token usage by running a 2-week pilot with full logging enabled. Measure actual prompt lengths (not estimated), actual response lengths (often 2-4x longer than expected), error retry rates (typically 5-10% additional tokens), and peak vs. average usage patterns (spikes can be 3-10x average).

Most organizations underestimate output tokens by 200-300% because they assume concise responses, but GPT-4 generates verbose explanations unless specifically prompted otherwise.

**Measurement methodology:**

**Step 1: Enable comprehensive logging**
```bash
# Azure Monitor diagnostic settings
az monitor diagnostic-settings create \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account} \
  --name openai-token-tracking \
  --logs '[{"category":"RequestResponse","enabled":true}]' \
  --workspace /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{workspace}
```

**Step 2: Track key metrics per use case**
- Input token average and distribution
- Output token average and distribution  
- Input/output ratio (critical for cost projection)
- Error rate and retry overhead
- Peak usage vs. average (capacity planning)

**Step 3: Query usage patterns**
```kusto
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.COGNITIVESERVICES"
| where OperationName == "OpenAI.ChatCompletions"
| extend InputTokens = toint(properties_s.usage_prompt_tokens)
| extend OutputTokens = toint(properties_s.usage_completion_tokens)
| summarize 
    AvgInput = avg(InputTokens),
    AvgOutput = avg(OutputTokens),
    P95Input = percentile(InputTokens, 95),
    P95Output = percentile(OutputTokens, 95),
    TotalCalls = count()
    by ApplicationName = tostring(tags_s.Application)
```

**Step 4: Calculate monthly projection**
```
Monthly Cost Projection = 
  [(Avg Daily Input Tokens × 30) × Input Token Price] +
  [(Avg Daily Output Tokens × 30) × Output Token Price] +
  [(Error Retry Rate × Total Token Cost)] +
  [(Peak Buffer 20% × Total Token Cost)]
```

**Real example from our pilot:**
- Estimated: 50M tokens/month ($1,250 calculated cost)
- Measured after 2 weeks:
  - Input: 10M tokens/month (matched estimate)
  - Output: 45M tokens/month (3x higher than estimated)
  - Retry overhead: 8% additional
  - Peak spikes: 2.5x average during business hours
- **Actual projected cost: $2,700/month**

The ratio matters more than volume. Track input/output ratio per use case:
- Customer support: averages 1:3 (input:output)
- Code generation: averages 1:4  
- Document summarization: averages 1:1.5
- Data extraction: averages 1:0.5

**Common measurement mistakes:**

❌ Estimating based on sample prompts instead of production traffic
❌ Assuming output length matches input length
❌ Ignoring error retries and failed requests
❌ Not accounting for peak usage multipliers
❌ Testing with controlled data instead of real user inputs

✅ Run pilot with actual users and production-like workloads
✅ Log every request for 2+ weeks to capture usage patterns
✅ Calculate P95 values, not just averages (spikes matter)
✅ Include buffer for growth and unexpected usage

Without measurement, you're guessing. With measurement, you're budgeting.

## How Can You Optimize Azure OpenAI Costs Without Sacrificing Quality?

Optimize costs through five strategic levers:

**1. Model selection** - Use GPT-3.5 for 80% of workloads, reserve GPT-4 for complex analysis. This saves 75% on token costs for routine tasks.

**2. Prompt engineering** - Reduce average prompt from 800 tokens to 300 tokens through context compression and pre-processing. This delivers 62% input cost reduction.

**3. Output control** - Specify maximum response lengths in prompts, use structured output formats instead of verbose explanations. This achieves 40-60% output reduction.

**4. Caching strategy** - Cache common responses at application layer, reuse results for identical queries. This provides 30-50% token reduction for repeated queries.

**5. Error reduction** - Implement retry logic with exponential backoff, validate inputs before API calls to reduce wasted tokens on malformed requests. This eliminates 5-10% waste.

Combined optimization across all five levers typically reduces [Azure OpenAI costs](/blog/azure-openai-pricing-real-costs/) by 60-70% without degrading quality. Start with model selection (biggest impact, easiest implementation), then prompt engineering, then output control.

**Optimization priority and impact:**

| Strategy | Effort | Cost Reduction | Time to Implement |
|----------|--------|----------------|-------------------|
| Model selection | Low | 60-75% | 1 week |
| Prompt engineering | Medium | 40-62% | 2-3 weeks |
| Output control | Low | 40-60% | 1 week |
| Response caching | Medium | 30-50% | 2 weeks |
| Error reduction | Low | 5-10% | 1 week |

**Real optimization results from our environment:**

**Before optimization:**
- 100M tokens/month
- 100% GPT-4 Turbo
- Average prompt: 850 tokens
- Average response: 600 tokens
- No caching
- **Cost: $14,500/month**

**After optimization:**
- 100M tokens/month (same volume)
- 80% GPT-3.5, 20% GPT-4 Turbo
- Average prompt: 320 tokens (compressed)
- Average response: 280 tokens (controlled)
- 35% cache hit rate
- **Cost: $4,800/month**

**Savings: $9,700/month (67% reduction)**

The critical insight: optimization compounds. Each strategy independently reduces costs 30-60%, but combined they deliver 60-70% total reduction. Quality stayed consistent - we A/B tested model selection and prompt optimization with business users who couldn't detect the difference.

For comprehensive cost optimization strategies beyond token management, see our guide on [what actually works for Azure cost optimization](/blog/azure-cost-optimization-complete-guide/) covering Reserved Instances, right-sizing, and architectural decisions.

## The Questions to Ask Before You Deploy

Before you commit to Azure OpenAI:

**1. "What's my actual token usage pattern?"**
- Run a 2-week pilot with logging
- Measure real input/output ratios
- Don't trust estimates - measure

**2. "Do I need fine-tuning or can I use prompt engineering?"**
- Fine-tuning costs $1,836/month minimum (December 2025)
- Better prompts cost $0
- Test prompt optimization first

**3. "Can I use GPT-3.5 or GPT-4o instead of GPT-4 Turbo?"**
- Run the same tasks through all models
- Measure quality difference
- Calculate if GPT-4's improvement is worth 4-7.5x cost

**4. "What's my actual monthly volume?"**
- If >$5K/month, talk to Microsoft about PTUs
- If <$5K/month, use pay-as-you-go
- Calculate breakpoint for your workload

**5. "What infrastructure do I actually need?"**
- Private endpoints? ($7.20/month each)
- Geo-redundancy? (doubles costs)
- Custom domains? (Key Vault + traffic manager)

## The Bottom Line

Microsoft's pricing calculator is a starting point. Not the actual cost.

**For most production workloads:**
- Calculator estimate: X
- Actual cost: 1.3X to 2X

**For workloads with fine-tuning:**
- Calculator estimate: X  
- Actual cost: 2X to 4X

**Plan accordingly.**

[Azure OpenAI](/blog/azure-openai-pricing-real-costs/) cost management is a subset of enterprise Azure FinOps. For the complete framework covering cost visibility, optimization, and [governance](/blog/azure-governance-finops-hub/) across all Azure services, read our [Azure FinOps complete guide](/blog/azure-finops-complete-guide/).

The good news: Once you understand the real cost structure, you can optimize it. We reduced Azure OpenAI spend by 60% by:
- Switching 80% of workloads to GPT-3.5
- Deleting unused fine-tuned models
- Optimizing prompt token usage
- Negotiating PTU pricing for production

**But you can't optimize what you don't understand.**

And Microsoft's calculator doesn't give you understanding. It gives you an estimate that's off by $30K/year.

---

## Related Posts

**FinOps & Cost Management:**
- [Azure FinOps Complete Guide](/blog/azure-finops-complete-guide/) - Enterprise FinOps framework
- [Azure Cost Optimization: What Actually Works](/blog/azure-cost-optimization-complete-guide/) - Real tactics beyond Azure Advisor
- [Azure Costs: Track by Apps, Not Subscriptions](/blog/azure-costs-apps-not-subscriptions/) - Application-level cost visibility
- [Azure Chargeback Models](/blog/azure-chargeback-tags-model/) - Chargeback that business units accept
- [Why Finance Accepts Monthly OpEx for Phones but Not Cloud](/blog/finance-accepts-monthly-opex-phones-not-cloud/) - Navigating finance objections

**Governance & Tagging:**
- [Azure Resource Tagging Best Practices](/blog/azure-resource-tags-guide/) - Tag [governance](/blog/azure-governance-finops-hub/) for cost allocation
- [Azure Tag Governance: The 247 Variations Problem](/blog/tag-governance-247-variations/) - Solving tag standardization

**AI & Automation:**
- [Azure AI Foundry Terraform Guide](/blog/azure-ai-foundry-terraform/) - Infrastructure as Code for AI deployments

---

---

## Frequently Asked Questions About Azure OpenAI Pricing

### How much does Azure OpenAI cost per month?

For typical enterprise deployments, monthly costs range from $5,000 to $50,000 depending on:
- API call volume (most enterprises generate 500M-5B tokens/month)
- Model selection (GPT-4 Turbo costs 60x more than GPT-4o mini)
- Caching efficiency (uncached prompts cost 2x more)
- Embedding model usage for RAG implementations

Small pilot projects (< 100K requests/month) typically spend $500-$2,000/month.

### Is Azure OpenAI cheaper than OpenAI's direct API?

No. Azure OpenAI is approximately 10-15% more expensive than [OpenAI's](/blog/azure-openai-pricing-real-costs/) direct API. You pay the premium for:
- Private networking (no internet exposure)
- Enterprise SLA (99.9% uptime guarantee)
- Compliance certifications (SOC 2, HIPAA, FedRAMP)
- Regional data residency (EU, US, Asia)
- Integration with Azure services (Key Vault, Monitor, Defender)

For regulated industries (finance, healthcare, government), the premium is mandatory, not optional.

### What is the cheapest Azure OpenAI model in 2025?

GPT-4o mini is the most cost-effective model at:
- **Input:** $0.15/million tokens
- **Output:** $0.60/million tokens  
- **Average:** ~$0.50/million tokens for typical workloads

This is 60x cheaper than GPT-4 Turbo while maintaining 80-90% of the capability for most business use cases.

For basic tasks (classification, summarization, simple Q&A), GPT-4o mini provides the best price-performance ratio.

### Does Azure OpenAI charge for failed requests?

Partially. You're charged for:
- ✅ Tokens processed before an error (counted as billable)
- ✅ Rate limit errors after token processing started
- ❌ Authentication failures (not billable)
- ❌ Network timeouts before processing (not billable)

**Real impact:** If your application retries failed requests without exponential backoff, you can double your token costs. Always implement retry logic with delays.

### Can I get volume discounts for Azure OpenAI?

Yes, but not automatically. Volume discounts require:
- Enterprise Agreement (EA) with Microsoft
- Committed spend threshold (typically $100K+/year)
- Direct negotiation with Azure sales team

Typical discounts range from 10-30% for customers committing to $500K+/year spend. Small businesses on pay-as-you-go plans don't qualify.

### What's the cost difference between GPT-4 and GPT-4 Turbo?

**GPT-4:**
- Input: $30/million tokens
- Output: $60/million tokens

**GPT-4 Turbo:**
- Input: $10/million tokens
- Output: $30/million tokens

**GPT-4 Turbo is 3x cheaper than GPT-4** while being faster and supporting larger context windows (128K tokens vs 8K).

Unless you specifically need GPT-4's unique capabilities, GPT-4 Turbo is the better choice for cost optimization.

### Do embedding models cost extra?

Yes. Embedding models have separate pricing:
- **text-embedding-3-small:** $0.02/million tokens
- **text-embedding-3-large:** $0.13/million tokens
- **text-embedding-ada-002:** $0.10/million tokens

**Real scenario:** Building a RAG system for 10,000 documents (average 2,000 tokens each) costs:
- Initial embedding: 20M tokens × $0.02 = $400 one-time
- Incremental updates: $20-$100/month for new content

Most enterprises underestimate embedding costs by 50-80% because they forget to account for re-embedding updated content and vector database storage costs.

### How does Azure OpenAI pricing compare to building your own LLM?

**Self-hosted open-source LLM (Llama 2 70B):**
- Hardware: $50K-$150K upfront (8x A100 GPUs minimum)
- Monthly hosting: $5K-$15K (Azure VM compute)
- Engineering: 2-3 FTE ML engineers ($300K-$450K/year)
- **Break-even:** Need $50K+/month [Azure OpenAI](/blog/azure-openai-pricing-real-costs/) spend to justify

**Verdict:** Use Azure OpenAI unless you're spending $500K+/year AND have dedicated ML team.

### Can I pause Azure OpenAI resources to save money?

No. Azure OpenAI uses a "provisioned throughput" model where you pay for:
- Reserved capacity (even if unused)
- Token processing (consumption-based)

You cannot "pause" deployments like you can with VMs. To reduce costs:
- Delete unused deployments immediately
- Use autoscaling to match demand
- Consolidate workloads onto fewer deployments

**Trap:** Developers create test deployments and forget them. $5K/month in unused capacity is common.

---

## 🎯 Track Azure Costs Like a Pro

This guide covers [OpenAI pricing](/blog/azure-openai-pricing-real-costs/), but **managing costs across 30,000+ resources requires powerful KQL queries.**

**The Complete KQL Query Library includes:**
- ✅ 48 production-ready cost analysis queries
- ✅ Track spending by subscription, resource group, tag
- ✅ Identify unused resources costing you thousands
- ✅ Enterprise-scale tested patterns
- ✅ Lifetime updates

**Launch price: $19** (regular $29)

[Get the Complete KQL Library →](https://davidnoob.gumroad.com/l/hooih)

---

## 🛑 Don't Let AI Bankruptcy Be Your Strategy

You can't manage AI costs if you don't know who owns the AI.
Is it the App Team? The Data Team? The Cloud Platform Team?

Stop guessing. Define the ownership structure explicitly before you deploy your next model.

**[Download the IT Roles & Responsibilities Matrix](/blog/it-roles-responsibilities-matrix/)** to see exactly how to assign AI cost accountability.

Or get the **Complete RACI Template** to deploy the [governance](/blog/azure-governance-finops-hub/) model immediately:

<div class="downloads" style="text-align: center; margin-top: 2rem;">
  <a class="btn" href="https://davidnoob.gumroad.com/l/ifojm?ref=openai-pricing-post" style="font-size: 1.2em; padding: 15px 30px; background-color: #0078d4; color: white;">Download RACI Template & AI Roles</a>
</div>

---

**Questions? Spot an error? Let me know in the comments below.**

*Updated December 30, 2025 with interactive calculator, FAQ section, and current pricing.*
