# Exercise: First API Call + Cost Calculation

**Day 1 — AI/LLM Application Development Course**

---

## Part 1: Your First Gemini API Call (30 min)

### Objective

Make your first programmatic call to Google's Gemini API using Python and observe how the API works — request, response, and token usage.

Read the README.md file in this folder to get detailed instructions on how to set up your environment and run the starter code. Then, experiment with different prompts and observe how token usage changes.

### Task


**Experiment.** Try changing the prompt to something longer or more complex. Observe how the token counts change. You can observe token usage from Google AI Studio. Try at least 3 different prompts and note the token counts.

| Prompt (short description) | Input Tokens | Output Tokens | Total Tokens |
|---|---|---|---|
| "Explain what an API is in 2 sentences" | | | |
| Your prompt #2 | | | |
| Your prompt #3 | | | |

### Reflection Questions

- How does prompt length relate to input token count?
- How does the complexity/length of the requested output affect output tokens?
- What happens if you ask the same question twice — do you get the same response? The same token count?

---

## Part 2: API Cost Calculation (30 min)

### Scenario

You are building a customer service chatbot. Your business requirements are:

- **500 users per day**
- **Each conversation averages ~2,000 tokens** (combined input + output)
- Assume roughly **50% input tokens, 50% output tokens** (1,000 input + 1,000 output per conversation)
- The chatbot runs **30 days per month**

### Your Task

Calculate the **monthly cost** of running this chatbot with three different providers. For each provider, pick **two models** (one cheaper, one more capable).

**You must find the current pricing yourself** from the official pricing pages:

- Google Gemini: https://ai.google.dev/gemini-api/docs/pricing
- OpenAI: https://openai.com/api/pricing
- Anthropic: https://docs.anthropic.com/en/docs/about-claude/models

> **Hint:** API pricing is typically listed as cost **per 1 million tokens**, with separate prices for input and output tokens.

### Step-by-Step Calculation Guide

**Step 1 — Calculate monthly token volume**

```
Daily conversations:         500
Tokens per conversation:     2,000
Days per month:              30

Monthly total tokens = 500 × 2,000 × 30 = 30,000,000 tokens (30M)

Of which:
  Input tokens  = 15,000,000 (15M)
  Output tokens = 15,000,000 (15M)
```

**Step 2 — Fill in the table below**

| Provider | Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) | Monthly Input Cost | Monthly Output Cost | **Monthly Total** |
|---|---|---|---|---|---|---|
| Google | _____________ | $_____ | $_____ | $_____ | $_____ | **$_____** |
| Google | _____________ | $_____ | $_____ | $_____ | $_____ | **$_____** |
| OpenAI | _____________ | $_____ | $_____ | $_____ | $_____ | **$_____** |
| OpenAI | _____________ | $_____ | $_____ | $_____ | $_____ | **$_____** |
| Anthropic | _____________ | $_____ | $_____ | $_____ | $_____ | **$_____** |
| Anthropic | _____________ | $_____ | $_____ | $_____ | $_____ | **$_____** |

---

## Part 3: Discussion & Analysis (15 min)

Answer the following questions. Be prepared to discuss in class.

**1. Cost differences**
Which model was the cheapest and which was the most expensive in your calculations? How many times cheaper is the cheapest option compared to the most expensive? What does this tell you about model selection for production applications?

**2. Scaling scenario**
What if your chatbot grows to 5,000 users/day instead of 500? What would the monthly cost be for each model? At what point does cost become a real business concern?

**3. The input/output ratio matters**
In our scenario we assumed 50/50 input vs output tokens. In reality, chatbots often have much more output than input (the AI writes longer responses than the user's questions). Recalculate for your cheapest and most expensive model assuming **30% input / 70% output** (600 input + 1,400 output tokens per conversation). How does this change the cost picture?

**4. Beyond token price**
Cost per token is not the only factor when choosing a model. What other factors should you consider? Think about at least 3 factors beyond price.

**5. Free tiers and prototyping**
Several providers offer free tiers with rate limits. Look at the free tier for the provider you used in Part 1. Could the free tier handle our 500 users/day scenario? Why or why not?

---

## Bonus Challenge

Write a Python script that:
1. Takes a prompt as input
2. Sends it to the Gemini API
3. Prints the response
4. Calculates and prints the estimated cost of that single request using Gemini 2.5 Flash pricing

```python
# Skeleton to get you started:

def calculate_cost(input_tokens, output_tokens):
    """Calculate cost in USD using Gemini 2.5 Flash pricing."""
    input_price_per_million = 0.30
    output_price_per_million = 2.50
    
    cost = (input_tokens / 1_000_000 * input_price_per_million) + \
           (output_tokens / 1_000_000 * output_price_per_million)
    return cost

# Your code here: get response from API, extract token counts,
# call calculate_cost(), and print the result
```

---

*Official pricing pages for reference:*
- *Google Gemini: https://ai.google.dev/gemini-api/docs/pricing*
- *OpenAI: https://openai.com/api/pricing*
- *Anthropic: https://docs.anthropic.com/en/docs/about-claude/models*
