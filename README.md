# Cryptocurrency Curriculum Platform

> An educational platform for teaching blockchain and cryptocurrency concepts to complete beginners, developed for Universal Tech Movement (Austin, TX)

## 🎯 Project Overview

This project provides a comprehensive, full-stack educational platform for cryptocurrency and blockchain education. The curriculum takes students from absolute beginners to advanced developers capable of building their own blockchain applications and AI-powered trading bots.

## 📚 Curriculum Structure

### Part 1: The "User" Track (Foundations) ✅ COMPLETE
**Goal**: Create an informed, safe, and competent user of Web3

- **Module 1**: Blockchain Technology (2h)
- **Module 2**: Web3 Wallets & Security (3h)
- **Module 3**: Transactions, dApps & Gas Fees (1h)
- **Module 4**: Tokens & Digital Assets (3h)
- **Module 5**: Trading (2h)
- **Module 6**: DeFi & DAOs (2.5h)
- **Module 7**: Advanced Concepts Overview (2.5h)

### Part 2: The "Power User" / Analyst Track ⏳ IN PROGRESS
**Goal**: Bridge the gap from using the chain to analyzing it

- **Module 8**: Practical On-Chain Analysis
- **Module 9**: Advanced Market & Tokenomic Analysis
- **Module 10**: Advanced DeFi Strategies

### Part 3: The "Developer" Track ⏳ PENDING
**Goal**: Build technical skills for smart contracts and dApps

- **Module 11**: Development & Programming Prerequisites
- **Module 12**: Smart Contract Development (Solidity & EVM)
- **Module 13**: dApp Development & Tooling

### Part 4: The "Architect" / Builder Track ⏳ PENDING
**Goal**: Use developer skills to build complex, novel systems

- **Module 14**: Creating a Fungible Token & ICO
- **Module 15**: Creating an NFT Collection & Marketplace
- **Module 16**: Building Your Own Blockchain & Mining
- **Module 17**: AI Agent Trading Bot Development (NEW!)

## 🏗️ Technical Architecture

### Frontend Stack
- **Framework**: React 18.3 with TypeScript
- **Build Tool**: Vite 5.4
- **UI Library**: Material-UI (MUI) v7
- **Styling**: Tailwind CSS + Emotion
- **Routing**: React Router v6
- **API Client**: Axios (port 8000)

### Backend Stack
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Database**: PostgreSQL 15+
- **Validation**: Pydantic v2
- **Authentication**: JWT
- **Testing**: Pytest

### AI Trading Bot Framework
- **Architecture**: Custom LLM-agnostic agent system
- **Supported LLMs**: OpenAI, Anthropic Claude, Ollama (local)
- **Features**: Technical indicators, backtesting, risk management
- **Design**: Educational, extensible, provider-agnostic

## 🤖 AI Agent Development System

This project uses a specialized AI agent framework in Cursor for efficient development:

### Specialized Agents
1. **Master Orchestrator** - Coordinates all development
2. **Frontend Component Agent** - React + TypeScript + MUI
3. **Backend API Agent** - FastAPI + SQLAlchemy
4. **Database Schema Agent** - PostgreSQL models & migrations
5. **Trading Bot Framework Agent** - AI trading bot system

📖 **Full documentation**: See [`cursor/AI_AGENT_SYSTEM.md`](cursor/AI_AGENT_SYSTEM.md)

## 📁 Project Structure

```
crypto-curriculum/
├── .gitignore                    # Git ignore rules (API keys, secrets, etc.)
├── README.md                     # This file - Project overview
├── DEVELOPMENT_QUICKSTART.md     # Quick start guide for developers
│
├── curriculum/                   # 📚 All curriculum content
│   ├── code-examples/           # Reference code for teaching
│   │   └── module-17/           # AI agent examples (Python)
│   ├── blockchain curriculum outline.md
│   ├── blockchain curriculum part 1.md (✅ Complete)
│   ├── blockchain curriculum part 2.md (✅ Complete)
│   ├── blockchain curriculum part 3.md (✅ Complete)
│   └── blockchain curriculum part 4.md (✅ Complete)
│
├── app/                          # 💻 Application code (to be initialized)
│   ├── frontend/                 # React application
│   │   ├── src/
│   │   │   ├── components/      # Reusable UI components
│   │   │   ├── pages/           # Page components (routes)
│   │   │   ├── modules/         # Module-specific content
│   │   │   ├── services/        # API service layer
│   │   │   ├── types/           # TypeScript interfaces
│   │   │   ├── hooks/           # Custom React hooks
│   │   │   ├── utils/           # Helper functions
│   │   │   ├── theme/           # MUI + Liquid Glass theme
│   │   │   └── App.tsx
│   │   ├── public/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── README.md            # Frontend-specific docs
│   │
│   └── backend/                  # FastAPI application
│       ├── api/                  # API routes
│       │   └── v1/endpoints/
│       ├── services/             # Business logic layer
│       ├── models/               # SQLAlchemy models
│       ├── schemas/              # Pydantic schemas
│       ├── core/                 # Config, database, security
│       ├── ai_agent/             # Trading bot framework
│       │   ├── base_agent.py
│       │   ├── llm_provider.py
│       │   ├── providers/       # OpenAI, Anthropic, Ollama
│       │   └── tools/           # Trading tools
│       ├── utils/
│       ├── tests/
│       ├── main.py
│       ├── requirements.txt
│       └── README.md            # Backend-specific docs
│
├── cursor/                       # 🤖 AI agent configurations
│   ├── AI_AGENT_SYSTEM.md       # Agent system documentation
│   └── rules/                    # Agent rule files
│       ├── masterOrchestrator.mdc
│       ├── frontendComponentAgent.mdc
│       ├── backendApiAgent.mdc
│       ├── databaseSchemaAgent.mdc
│       └── tradingBotAgent.mdc
│
├── dev/                          # 🎨 Design examples & prototypes
│   ├── part 1 webpage example.html
│   └── part 1 infographic example.html
│
├── docs/                         # 📖 Project documentation
│   ├── api/                      # API documentation
│   ├── deployment/               # Deployment guides
│   ├── architecture/             # System diagrams & design docs
│   ├── guides/                   # Developer & user guides
│   └── README.md                 # Documentation guidelines
│
└── scripts/                      # 🔧 Automation scripts
    ├── setup-dev.sh              # Development setup (to create)
    ├── init-db.sh                # Database initialization (to create)
    └── README.md                 # Script guidelines
```

### 📝 Directory Guidelines

**Where to put files:**

| File Type | Location | Example |
|-----------|----------|---------|
| Curriculum content | `curriculum/` | Markdown lesson files |
| Teaching code examples | `curriculum/code-examples/` | Python examples for Module 17 |
| Application source code | `app/frontend/` or `app/backend/` | React components, API routes |
| Component-specific docs | Component's `README.md` | `app/frontend/README.md` |
| Project-wide documentation | `docs/` | API specs, architecture diagrams |
| Automation scripts | `scripts/` | Setup, deployment, database scripts |
| AI agent configurations | `cursor/` | Agent rule files |
| Design references | `dev/` | HTML examples, mockups |

**Note:** READMEs can stay in their relevant directories (e.g., `app/frontend/README.md`), but comprehensive documentation belongs in `docs/`.

## 🎓 Key Features

### For Students
- **Progressive Learning**: Four tracks from beginner to architect
- **Interactive Content**: Engaging lessons with visualizations
- **Hands-on Practice**: Coding exercises and real projects
- **Progress Tracking**: Track completion through modules
- **Assessments**: 10 questions/tasks per module (170 total)
- **AI Trading Bot**: Build and customize your own trading bot

### For Teachers
- **Admin Dashboard**: Manage students and content
- **Progress Monitoring**: Track student completion and scores
- **Content Management**: Update curriculum materials
- **Analytics**: View engagement and performance metrics

### Technical Highlights
- **Full TypeScript**: Type-safe frontend and API contracts
- **Async Architecture**: Non-blocking operations throughout
- **LLM-Agnostic Bot**: Works with any LLM provider
- **Responsive Design**: Mobile-first, accessible interface
- **RESTful API**: Clean, well-documented endpoints
- **Database Migrations**: Version-controlled schema changes

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 15+
- Git

### Installation

#### Frontend Setup
```bash
cd app/frontend
npm install
npm run dev
```

#### Backend Setup
```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000
```

#### Database Setup
```bash
# Create PostgreSQL database
createdb crypto_curriculum

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/crypto_curriculum"
export SECRET_KEY="your-secret-key"
export LLM_API_KEY="your-llm-api-key"
```

## 📝 Content Development

Each curriculum module follows a structured template:

1. **Core Definition**: Clear, simple explanation
2. **Simple Analogies**: Minimum 2 relatable analogies
3. **Key Talking Points**: Exhaustive itemized list
4. **Step-by-Step Process**: How it works (if applicable)
5. **Relevance/Importance**: Why it matters
6. **Pros & Cons**: Balanced view of trade-offs
7. **Common Misconceptions**: What beginners get wrong
8. **Critical Warnings**: Security and financial risks
9. **Assessment**: 10 questions/tasks per module

See [`curriculum/blockchain curriculum part 1.md`](curriculum/blockchain curriculum part 1.md) for complete example.

## 🧪 Testing

### Frontend Tests
```bash
cd app/frontend
npm run test
npm run test:coverage
```

### Backend Tests
```bash
cd app/backend
pytest
pytest --cov=app
```

### E2E Tests
```bash
npm run test:e2e
```

## 🐳 Docker Deployment

```bash
# Build containers
docker-compose build

# Run services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📊 Current Status

### ✅ Completed
- [x] Project structure and planning
- [x] AI agent system setup
- [x] Curriculum Part 1 detailed content (Modules 1-7)
- [x] Design examples and prototypes
- [x] Agent configuration files
- [x] Documentation framework

### ⏳ In Progress
- [ ] Curriculum Part 2 (Modules 8-10)
- [ ] Curriculum Part 3 (Modules 11-13)
- [ ] Curriculum Part 4 (Modules 14-17)
- [ ] Testing components (170 questions/tasks)

### 📋 Upcoming
- [ ] Project initialization (frontend + backend)
- [ ] Database schema implementation
- [ ] API development
- [ ] Frontend components
- [ ] AI trading bot framework
- [ ] Content integration
- [ ] Testing and deployment

## 🤝 Contributing

This project is developed for Universal Tech Movement in Austin, TX. For questions or contributions, please contact the project maintainers.

## 📄 License

[To be determined based on organization requirements]

## 🙏 Acknowledgments

- **Universal Tech Movement** - Austin, TX non-profit organization
- **Target Audience** - Complete beginners with no technical background
- **Educational Focus** - Comprehensive, accessible, practical learning

---

**Built with ❤️ for the next generation of blockchain developers**

