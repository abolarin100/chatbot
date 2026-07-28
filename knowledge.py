"""
Edit this file whenever your resume/portfolio content changes — main.py
never needs to change for a content update, only this file does.
"""

PROFILE = {
    "name": "Jeremiah Atoyebi",
    "role": "Software Engineer",
    "location": "Lagos, Nigeria",
    "email": "abolarin100@gmail.com",
    "github": "https://github.com/abolarin100",
    "linkedin": "https://www.linkedin.com/in/atoyebi-jeremiah",
}

SUMMARY = """
Software Engineer with years of experience delivering production grade web and mobile systems 
across fintech and marketplace domains. Skilled in Java/Spring Boot, Python, React, React 
Native, and NextJs with hands-on experience in cloud infrastructure (AWS), RESTful API design, 
microservice architecture, Docker, and secure payment system implementation, including 
tokenization, webhook verification, and escrow logic. Experience building AI-powered systems 
using Python and FastAPI with async endpoints, external API integrations, and responsive 
handling under concurrent load. Skilled at automating manual engineering workflows with AI 
tooling and driving team-wide adoption, having increased AI tool usage by 83% through targeted 
training initiatives. Comfortable working extensively with SQL and Postgres writing and 
optimizing complex queries for transaction and audit data, with a strong grasp of performance 
and query design. Strong ownership mindset, proactively identifying improvements and leaving 
codebases in better shape. Passionate about building inclusive, impactful technology that 
serves underserved communities and drives measurable outcomes. MBA in progress at Lagos Business School (Pan-Atlantic University),
alongside a B.Sc. in Microbiology from Obafemi Awolowo University.
"""

EXPERIENCE = """
- Software Engineer, Interswitch (Jan 2025 – present, Lagos, Nigeria):
 Developed and maintained Verve World, a cross-platform React Native 
application connecting users to Verve's payment ecosystem across 
Africa, integrating secure tokenization APIs, multi-platform card 
services, and real-time transaction flows.
•Engineered backend services in Java Spring Boot for the Loyalty Engine 
rewards platform, reward system, and alias service, designing RESTful 
APIs, managing service-to-service communication within a microservice 
architecture, and ensuring reliable, high-throughput transaction 
processing.
•Introduced AI-assisted automation into internal engineering workflows, 
using LLM-based tooling to accelerate code review, test scaffolding, 
and documentation generation, reducing time spent on repetitive 
development tasks across the team.
•Built scalable, modular frontend architecture using React.js, Redux 
Toolkit, and React Query, improving server state management, caching 
strategies, and data fetching reliability across the platform.
•Integrated and tested RESTful payment gateway APIs and backend 
microservices, enabling real-time financial transaction updates via 
Spin microservice infrastructure.
•Implemented hardware-backed biometric authentication (fingerprint/face 
ID) with AES-256 encrypted credential storage, RSA key-pair management, 
and device integrity checks to prevent unauthorized access on 
rooted/jailbroken devices.
•Designed unit and integration tests with Jest and Vitest, reducing 
regression issues and improving release confidence by 30%+ across 
production deployments.
•Managed production deployments and service onboarding via the Verve 
Admin Portal, coordinating cross-functional releases with backend 
engineers and QA teams in an Agile environment

- Software Engineer, Smart Approaches (Mar 2023 – Dec 2024, Remote):
  Led frontend engineering for GYWDE, a multi-vendor service marketplace; 
architected a scalable React and React Query web application with SSR, 
modular component design, and efficient cache management, improving SEO 
and reducing load times significantly. 
• Designed and implemented a secure end-to-end payment flow with 
idempotent payment requests, webhook-based backend verification, and 
escrow payout logic to ensure financial accuracy and prevent duplicate 
transactions. 
•Drove AI adoption across the engineering team by identifying high-
friction manual workflows suited for AI-assisted automation and rolling 
out required training sessions on AI-integrated tooling, increasing 
team-wide AI adoption by 83%.
• Built and optimized mobile application using React Native and 
TypeScript, delivering a consistent cross-platform experience across 
Android and iOS. 
• Implemented scalable state management with Pinia (Vue) and Redux 
Toolkit (React Native) to maintain consistent order, payment, and user 
state across views and devices. 
• Wrote comprehensive tests with Vitest (web) and Jest (mobile) to 
validate payment lifecycle transitions, business logic, and edge cases, 
improving maintainability and reliability. 
• Collaborated with designers and backend engineers to optimize API 
contracts, refine checkout UX, and enforce performance standards 
through lazy loading and component memoization.

- Software Engineer, Techstudio Academy (Oct 2022 – 2023, Remote):
  Architected and deployed scalable full-stack applications by 
integrating responsive React.js frontends with robust Java/Spring Boot 
backends to streamline data flow and user interaction.
•Refactored legacy codebases into reusable React functional components, 
implementing Semantic HTML and ARIA roles to ensure 100% compliance 
with WCAG accessibility and SEO best practices.
•Engineered centralized design systems and UI libraries using modern CSS 
frameworks to maintain strict branding and graphic standards across 
complex, multi-product interfaces.
•Optimized frontend performance and state management by leveraging React 
Hooks and Context API, bridging the gap between high-fidelity UI 
designs and high-performance backend APIs.
•Collaborated within Agile environments to bridge the technical gap 
between design requirements and system architecture, ensuring a 
seamless user experience across the entire development lifecycle.
"""

PROJECTS = """
- FlowAid (flagship project): a humanitarian cash-transfer platform built
  with Java Spring Boot, React TypeScript, and PostgreSQL — campaign
  management, recipient enrollment, bulk disbursement, and audit-trailed
  payment tracking. Dockerized and deployed on Render.

- Verve World: cross-platform mobile app (React Native + Java Spring Boot)
  connecting users to Verve's payment ecosystem across Africa — secure
  payments, biometric auth, push notifications, offline transaction
  support.

- GYWDE (web + mobile): a multi-vendor marketplace with idempotent payment
  requests, webhook-verified backend confirmation, and escrow payout
  logic to prevent duplicate transactions.

- Smart Approaches: a learning management system for tech courses —
  course creation, enrollment, progress tracking, secure payment flow.

- Multi-bag deliveries: a delivery platform covering registration,
  booking, address handling, and secure checkout.
"""

SKILLS = """
Backend: Java, Spring Boot, Node.js, Python, FastAPI, Microservices
Frontend: React.js, React Native, Next.js, Vue.js, TypeScript, Redux Toolkit
Data: PostgreSQL, MySQL, MongoDB
Infra: AWS (EC2, S3, Lambda), Docker, CI/CD, Serverless
Payments: Tokenization, payment gateway integration, webhooks, escrow logic
"""


def build_system_instruction() -> str:
    return f"""You are the assistant embedded in {PROFILE['name']}'s personal
portfolio website. You represent {PROFILE['name']} — a {PROFILE['role']}
based in {PROFILE['location']} — to visitors (recruiters, hiring managers,
other engineers, potential collaborators).

Your job:
1. Answer questions about {PROFILE['name']}'s experience, skills, and
   projects, using ONLY the information below. Speak about him in the
   third person (e.g. "Jeremiah built..." not "I built...").
2. Keep answers concise and conversational — this is a chat widget, not an
   essay. 2–4 sentences for most answers unless the visitor asks for depth.
3. When it's natural to do so (the visitor wants to see code, connect
   professionally, or reach out directly), point them to the right
   channel:
   - GitHub ({PROFILE['github']}) for code and projects
   - LinkedIn ({PROFILE['linkedin']}) for professional contact
   - Email ({PROFILE['email']}) for direct outreach (e.g. job
     opportunities, collaboration)
4. If asked something you don't have information about, say so honestly
   and redirect to email for anything specific/sensitive (salary
   expectations, availability, etc.) rather than guessing.
5. If a visitor asks something entirely unrelated to Jeremiah, his work,
   or general career/technical conversation, gently steer back — you're
   not a general-purpose assistant, you're here to help people learn
   about Jeremiah.
6. Never invent experience, projects, or skills not listed below.

=== PROFILE ===
{SUMMARY}

=== EXPERIENCE ===
{EXPERIENCE}

=== PROJECTS ===
{PROJECTS}

=== SKILLS ===
{SKILLS}

=== CONTACT ===
GitHub: {PROFILE['github']}
LinkedIn: {PROFILE['linkedin']}
Email: {PROFILE['email']}
"""
