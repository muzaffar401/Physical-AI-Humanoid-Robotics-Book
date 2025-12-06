---
id: api-keys-setup
title: API Keys Setup
sidebar_label: API Keys Setup
unlisted: true
displayed_sidebar: null
---

# API Keys Setup

Module 4 requires API keys for AI services. Follow these steps to set up your environment securely.

### Required Services

You need **ONE** of the following combinations:

**Option A: OpenAI Only** (Whisper + GPT-4)
- OpenAI API key for both speech-to-text (Whisper) and task planning (GPT-4)
- Cost: ~$5-10 for full module completion
- Sign up: https://platform.openai.com/signup

**Option B: OpenAI + Anthropic** (Whisper + Claude)
- OpenAI API key for Whisper (speech-to-text)
- Anthropic API key for Claude 3 (task planning, alternative to GPT-4)
- Cost: ~$5-10 for full module completion
- Sign up: https://platform.openai.com/signup and https://console.anthropic.com/

### Step-by-Step Setup

#### 1. Create API Accounts

**For OpenAI**:
1. Visit https://platform.openai.com/signup
2. Create account and verify email
3. Add payment method (Settings → Billing → Payment Methods)
4. New accounts get $5 free credit (usually sufficient for this module)

**For Anthropic** (optional, if using Claude instead of GPT-4):
1. Visit https://console.anthropic.com/
2. Create account and verify email
3. Add payment method (Settings → Billing)
4. No free tier, but competitive pricing

#### 2. Generate API Keys

**OpenAI**:
1. Navigate to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Give it a name (e.g., "Module 4 - VLA")
4. **Copy the key immediately** (starts with `sk-proj-...`) - you won't see it again!

**Anthropic** (if using):
1. Navigate to https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. **Copy the key** (starts with `sk-ant-...`)

#### 3. Store Keys Securely in `.env` File

Create a `.env` file in your workspace root:

```bash
cd ~/ros2_ws/src/vla_project  # Or your workspace path
nano .env  # Or use your preferred text editor
```

**For OpenAI (Whisper + GPT-4)**:
```bash
# .env file
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
WHISPER_MODE=api
```

**For Anthropic (Claude) + OpenAI (Whisper)**:
```bash
# .env file
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
WHISPER_MODE=api
```

#### 4. Secure Your `.env` File

**CRITICAL**: Never commit `.env` to version control!

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env*.local" >> .gitignore

# Verify .env is ignored
git status  # .env should NOT appear
```

#### 5. Test API Keys

```bash
# Activate your virtual environment (if using one)
source venv/bin/activate

# Test OpenAI API
python3 << EOF
import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test with a simple completion
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Say 'API works!'"}],
    max_tokens=10
)
print("✅ OpenAI API:", response.choices[0].message.content)
EOF

# Test Anthropic API (if using Claude)
python3 << EOF
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=10,
    messages=[{"role": "user", "content": "Say 'API works!'"}]
)
print("✅ Anthropic API:", response.content[0].text)
EOF
```

If both tests print `✅ API works!`, you're ready to proceed!

### Cost Monitoring

Monitor your API usage to avoid unexpected charges:

**OpenAI Dashboard**: https://platform.openai.com/account/usage
**Anthropic Dashboard**: https://console.anthropic.com/settings/usage

**Set Usage Limits** (Recommended):
1. OpenAI: Settings → Billing → Usage limits → Set monthly limit (e.g., $20)
2. Anthropic: Settings → Usage → Set budget alerts

### Alternative: Local Models (No API Costs)

If you prefer not to use cloud APIs:

**Whisper**: Use local models instead of API
```bash
# .env
WHISPER_MODE=local
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large
```

**LLM**: Use local models (advanced, requires powerful GPU)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run local LLM
ollama run llama3:7b

# Update code to use Ollama API (localhost:11434)
```

**Trade-offs**:
- ✅ No API costs
- ✅ Full privacy (data never leaves your machine)
- ❌ Requires GPU (16GB+ VRAM for good LLM performance)
- ❌ Slower inference (local Whisper: 10-20s on CPU vs 1-2s API)
- ❌ Lower quality (local LLMs inferior to GPT-4/Claude for planning)

### Troubleshooting

**Error: "openai.AuthenticationError: Incorrect API key"**
- Check `.env` file has correct key (no quotes, no spaces)
- Verify key starts with `sk-proj-` (OpenAI) or `sk-ant-` (Anthropic)
- Regenerate key if compromised

**Error: "You exceeded your current quota"**
- You've hit spending limit or free credit exhausted
- Add payment method or increase usage limit

**Error: "Rate limit exceeded"**
- You're making requests too quickly (free tier: 3 req/min)
- Wait 60 seconds or upgrade to paid tier (200 req/min)

### Security Best Practices

1. **Never share API keys** (treat like passwords)
2. **Rotate keys regularly** (every 90 days)
3. **Use separate keys** for different projects (easier to track usage)
4. **Revoke unused keys** (delete old keys from dashboard)
5. **Monitor usage daily** (check for unauthorized use)

---

**Ready?** Once API keys are set up and tested, continue to the next chapter!
