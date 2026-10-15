<p align="center">
  <img src="./assets/artisan-banner.jpg" alt="Artisan Banner" width="800" />
</p>

# 🛡️ Artisan: The Autonomous AI Agent Operating System & Quality Protocol

> **Stop prompt-babysitting. Stop fixing AI stubs. Stop repeating past bugs.**  
> **Artisan** is the deterministic quality kernel, living neural memory, and multi-agent coordination protocol for modern AI coding assistants (Claude Code, Cursor, Copilot, Windsurf, Antigravity, Nous Hermes, Kimi). It turns probabilistic LLM generators into disciplined, self-auditing senior engineers.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](pyproject.toml)
[![CI/CD Tests](https://img.shields.io/badge/tests-520%2B%20passing-brightgreen.svg)](tests/)
[![Quality Gate](https://img.shields.io/badge/gatekeeper-100%2F100-success.svg)](scripts/pre-commit-gatekeeper.py)
[![Agents](https://img.shields.io/badge/supported%20agents-14%20ecosystems-cyan.svg)](#-supported-ai-agent-ecosystems)
[![MCP 2.0](https://img.shields.io/badge/MCP-JSON--RPC%202.0-orange.svg)](mcp/server.py)
[![Strategic Roadmap](https://img.shields.io/badge/roadmap-2026--2031-purple.svg)](docs/STRATEGIC_ROADMAP.md)
[![Live Playground](https://img.shields.io/badge/live%20demo-GitHub%20Pages-blue.svg)](https://kapitan00000978-sketch.github.io/artisan/)
[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<p align="center">
  <img src="./assets/artisan-demo.gif" alt="Artisan Protocol Liquid Glass Demo" width="800" style="border-radius: 14px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);" />
</p>

---

## ⚡ The Fundamental Shift: Standard AI vs. Artisan

```mermaid
graph LR
    subgraph Standard AI Assistant
        S1[User Prompt] --> S2[Probabilistic Output]
        S2 --> S3[// TODO: implement later]
        S2 --> S4[except: pass]
        S2 --> S5[Amnesia: Repeats Old Bugs]
    end

    subgraph Artisan Agent Operating System
        A1[User Prompt] --> A2[Context Engine & Memory]
        A2 --> A3[Autonomous Agent Execution]
        A3 --> A4[AST & Security Gatekeeper]
        A4 -->|Defect Detected| A5[Self-Healing Auto-Fix]
        A5 --> A4
        A4 -->|Clean 100/100| A6[Verified Commit & Learned Lesson]
    end
```

| Dimension | Standard AI Coding (Unmanaged) | With Artisan Protocol (v2.0) |
| :--- | :--- | :--- |
| **Code Completeness** | ❌ Leaves lazy `// TODO`, `FIXME`, or `pass` placeholders | ✅ **Zero-Defect AST Gate**: Rejects all stubs at pre-commit |
| **Error Handling** | ❌ Silently swallows errors (`except: pass`, empty `catch {}`) | ✅ **Self-Healing Engine**: Auto-refactors to structured logging |
| **Session Memory** | ❌ Total amnesia — forgets yesterday's bugs and decisions | ✅ **Living Memory Fabric**: `.artisan/memory.json` retains all scar tissue |
| **Multi-Agent Sync** | ❌ Claude, Cursor, and Copilot collide on the same files | ✅ **Swarm Registry**: `artisan agents` lock-free workspace coordination |
| **Token Efficiency** | ❌ 12,000+ token monolithic prompt dump | ✅ **Smart Context Engine**: 37x compression (~320 tokens per task) |
| **Human Babysitting** | ❌ Continuous *"You broke the build"* corrective loops | ✅ **100% Autonomous**: Passes 520+ tests before human delivery |

---

## 🌐 Live Interactive Playground

Experience real-time static code auditing, AST-based flaw detection, and autonomous remediation directly in your browser:  
👉 **[Open Live Playground](https://kapitan00000978-sketch.github.io/artisan/)**

---

## 📊 Synthetic Verification Suite (`bench/`)

Artisan provides a reproducible verification harness evaluating deterministic static detection and autonomous remediation across 10 controlled fixtures containing common AI anti-patterns (`python bench/run_benchmark.py`):

| Fixture Metric | Baseline AI Output (Without Gatekeeper) | With Artisan (Gatekeeper + Auto-Fix) |
| :--- | :--- | :--- |
| **Quality Gate Pass Rate** | `1 / 10` (10.0%) | **`10 / 10` (100.0%)** |
| **Defects Neutralized** | `0` (flaws leak into codebase) | **`9` anti-patterns deterministically resolved** |
| **Remediation Cycles** | Unbounded / Manual human triage | **Average `1.0` cycle auto-remediation** |

> Controlled evaluation methodology and task fixtures: [`bench/BENCHMARK_REPORT.md`](./bench/BENCHMARK_REPORT.md)

---

## ⚖️ When to Use vs. When to Skip (Decision Matrix)

| Scenario | Use Artisan? | Rationale |
| :--- | :---: | :--- |
| **Production or Team Codebases** | ✅ **YES** | Halts sloppy `TODO` stubs, silent `except: pass` leaks, and exposed API secrets before they enter the branch. |
| **Pair-Programming with AI Agents** | ✅ **YES** | Injects relentless engineering discipline into Claude Code, Cursor, Cline, Windsurf, and Kimi, eliminating repetitive prompt corrections. |
| **CI/CD Pipelines & Pre-Commit** | ✅ **YES** | Establishes an objective, deterministic, zero-compromise quality baseline across all Pull Requests. |
| **Quick 5-Minute Disposable Prototypes** | ❌ *Not Recommended* | If you are merely experimenting with a throwaway script, a strict pre-commit gate may add unnecessary friction. |
| **Pure Content / Markdown Writing** | ❌ *Not Recommended* | If the project contains no executable code, AST inspection and code quality gates are not required. |

---

## 📌 Project Overview & Architecture

**What is Artisan?**  
Artisan serves as the deterministic quality bridge between developers and autonomous AI coding agents (Claude Code, Cursor, Copilot, Windsurf, Antigravity, Cline, Kimi, and others). While modern foundation models generate code at incredible velocity, they lack innate quality discipline: unhandled edge cases, lazy `TODO` placeholders, silent exception swallowing (`except: pass`), unsafe `eval()` executions, or accidentally committed credentials frequently slip through.

Artisan resolves this systemic fragility across 5 core pillars:
1. **🛡️ Autonomous Pre-Commit & CI Gates (`scripts/detector.py`):** Conducts deep static analysis and AST (Abstract Syntax Tree) semantic inspection before code enters git. Commits are blocked if plaintext secrets (`sk-...`, `ghp_...`, `AKIA...`), dangerous injections, or unfinished stubs are detected.
2. **🔧 Self-Healing Remediation Engine (`artisan fix` / `scripts/remediator.py`):** Autonomously transforms silent catches (`except: pass` / `catch {}`) into structured logging and explicit error-handling pipelines without human intervention.
3. **🏛️ The Council of Masters (Senior Heuristics):** Injects the professional conscience and battle-tested criteria of **64 domain masters** spanning Architecture, Cryptography, Distributed Systems, Compilers, Robotics, HFT, Nuclear Physics, Tokamaks, Astrodynamics, and beyond.
4. **🧠 Persistent Project Memory (`.artisan/memory.json`):** Retains architectural conventions, team decisions, and historical scar tissue across sessions to prevent repeated errors.
5. **🔌 Model Context Protocol (MCP) Server (`mcp/server.py`):** Exposes live code inspection and domain persona retrieval as standard JSON-RPC 2.0 tools for Claude, Cursor, and any MCP-compliant assistant.

---

## 🎯 The Problem: Iterative Prompt Micromanagement
Developers often spend significant time micromanaging AI coding assistants:
- Base models may rush to generate boilerplate, occasionally leaving unfinished `TODO` stubs, unhandled boundary conditions, or unparameterized queries.
- Users frequently enter an iterative correction loop: *"Fix this error, you broke that import, handle this edge case."*
- **Artisan addresses this:** By embedding structured domain rules and automated quality checks directly into agent configuration files, the assistant self-audits before presenting results.

---

## 🔍 How It Works & Limitations

- **Session-Based Rules:** Rules files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) load per agent session into your assistant's system instructions.
- **Local Tooling:** The file sentinel watchdog (`scripts/watchdog.py`) and pre-commit gatekeeper (`scripts/pre-commit-gatekeeper.py`) are local command-line tools that run on your machine and in CI.
- **Limitations:** The gate catches the listed patterns (stubs, dangerous eval/exec, hardcoded secrets), not all bugs.
- **Demo Simulation Module:** The web engine in `src/engine/craftsmanshipEngine.js` is a non-functional, client-side interactive DEMO simulation for UI previewing; production enforcement is carried out by `scripts/detector.py` and the MCP server.

---

## 🏛️ The Council of Masters (Domain Heuristic Personas):

> [!NOTE]
> **Transparency & Architectural Modularity:**  
> The **Council of Masters** comprises 64 role-based synthetic domain personas and heuristic quality checklists inspired by open industry benchmarks (OWASP, ISO/IEC, SRE) and academic engineering literature. They are **not** real persons or claimed corporate employment affiliations.  
>  
> To eliminate context bloat, the 64 masters are organized into **8 Domain Guilds** (Software Architecture, Cybersecurity, UI/UX, Cloud DevOps, AI/LLMs, Business/Finance, Systems/Low-Level, and Deep-Tech Physics). When working on web apps or APIs, `SmartMasterSelector` dynamically loads only the 2–3 relevant software leads, reducing prompt overhead by over 80%. Specialized physics and deep-tech personas (Tokamaks, Geodynamo, Superfluid) serve as domain-specific simulation checklists for scientific computing codebases.

Artisan packages role-specific heuristics inspired by senior discipline leads:

| # | Master | Discipline & Role | Archetype | Core Focus |
| :- | :--- | :--- | :--- | :--- |
| 1 | 💻 **Marcus 'The Vanguard' Sterling** | Senior Software Architect & Systems Lead | Systems Sovereign & Zero-Tech-Debt Purist | SOLID architecture, zero unhandled stubs, concurrency |
| 2 | 🎯 **Diana 'The Closer' Drake** | Direct-Response Conversion Copywriter | Neuromarketing Alchemist & Persuasion Virtuoso | High-clarity hooks, value proposition, zero AI filler |
| 3 | 🎨 **Elena 'The Visionary' Rostova** | Principal UI/UX Designer & Systems Architect | Aesthetic Sovereign & Spatial Ergonomics Master | WCAG 2.1 AAA accessibility, 8pt spatial grid, design tokens |
| 4 | 📊 **Victor 'The Fortress' Montgomery** | Startup Financial Strategist & Fractional CFO | Unit-Economics Inquisitor & Capital Defense | Unit economics, burn rate, cash conversion cycles |
| 5 | ⚖️ **Arthur 'The Ironclad' Pendelton** | Senior Commercial Counsel & Contract Auditor | Commercial Safeguard & Contractual Litigator | Contract auditing, liability containment, clear definitions |
| 6 | 🔬 **Dr. Evelyn 'The Oracle' Reed** | Staff Data Scientist & ML Systems Architect | Empirical Scientist & ML Ops Gatekeeper | Data leakage prevention, statistical validation, model drift |
| 7 | 🛡️ **Gabriel 'The Sentinel' Frost** | Principal Cybersecurity & Offensive Auditor | Zero-Trust Inquisitor & Threat Modeling | OWASP Top 10, credential protection, parameterized queries |
| 8 | ⚡ **Gareth 'The Unbreakable' Drake** | DevOps & Cloud Site Reliability Architect | Chaos Engineering Commander & Reliability | Idempotent IaC, container best practices, health probes |
| 9 | 💎 **Kaelen 'The Shaper' Vane** | Principal 3D & Spatial CGI Artist | Spatial Shaper & PBR Master | Energy-conserving PBR shaders, quad topology, WebGL |
| 10 | 🎮 **Ronan 'The Engine' Blackwood** | Lead Game Systems & Physics Architect | Engine Virtuoso & Physics Pioneer | Fixed timestep integration, continuous collision, zero GC |
| 11 | 📱 **Lucas 'The Kinetic' Cruz** | Principal Mobile Systems Architect | Kinetic Craftsman & Gesture Lead | 120Hz ProMotion budget, 48dp touch targets, spring physics |
| 12 | ✨ **Aria 'The Luminary' Solano** | Global Brand Director & Visual Master | Visual Identity & Emotional Resonance | 60-30-10 color rule, modular type scales, vector viewBox |
| 13 | 🔊 **Damian 'The Resonant' Vance** | Principal Interactive Audio & Sound Architect | Soundscape Virtuoso & Audio Lead | Click-free exponential ramps, master dynamics limiter, ADSR |
| 14 | 🗄️ **Cassandra 'The Core' Thorne** | Principal Database & Distributed Data Architect | Data Sovereign & Low-Latency Lead | Sub-10ms query plans, zero N+1 loops, concurrent DDL |
| 15 | 🌐 **Zane 'The Vector' Sterling** | Technical SEO & Growth Engineering Lead | Algorithmic Vector & Discovery Lead | Core Web Vitals (CLS=0), single H1 hierarchy, Schema.org |
| 16 | 🧠 **Naomi 'The Neural' Chen** | Principal AI Agentic & LLM Architect | Autonomous Orchestration Sovereign | Deterministic JSON schemas, prompt injection shields, circuit breaker loops |
| 17 | ⚙️ **Valerie 'The Edge' Cross** | Principal Systems & Low-Level Performance Architect | Mechanical Sympathy & Low-Latency Sovereign | 64-byte cache alignment, zero heap allocs in hot loops, zero-copy slices, SIMD |
| 18 | 🌐 **Soren 'The Conductor' Lindqvist** | Principal Distributed Consensus & Protocol Architect | Distributed Consensus & Protocol Sovereign | Strict majority quorum ((N/2)+1), term fencing, re-entrancy locks (CEI), determinism |
| 19 | 🧬 **Nikolai 'The Core' Vance** | Principal Compiler & Type Systems Architect | Compiler Engineer & Type-Theoretic Sovereign | 100% exhaustive pattern matching, zero unsound escapes, recursion depth guard |
| 20 | 🛡️ **Seraphina 'The Aegis' Sterling** | Principal Quantum-Resistant Cryptographer | Quantum Aegis & Zero-Knowledge Sovereign | FIPS 203 ML-KEM lattice encapsulation, constant-time execution, ZKP nullifier deduplication |
| 21 | ⚡ **Thaddeus 'The Chrono' Vance** | Principal HFT & Event-Loop Architect | Deterministic Low-Jitter Sovereign | Zero-syscall busy polling, CPU core affinity pinning, wait-free SPSC ring buffers |
| 22 | 🦾 **Dr. Vespera 'The Kinematic' Sterling** | Principal Autonomous Robotics Architect | Real-Time Control Sovereign & Kinematic Purist | 1kHz actuation cycles, torque saturation envelopes, DLS singularity damping, EKF sensory fusion |
| 23 | ⚡ **Ignis 'The Silicon' Thorne** | Principal ASIC & FPGA Hardware Architect | Silicon Sovereign & RTL Synthesis Conscience | Latch-free combinational logic, dual-flop CDC synchronizers, STA positive slack, sync reset |
| 24 | ⚡ **Morpheus 'The Kernel' Vance** | Principal Embedded Firmware Architect | Bare-Metal Sovereign & Firmware Conscience | Zero-malloc static pools, sub-5µs deferred ISR, hardware WDT supervisor, DMA cache coherency |
| 25 | 🛰️ **Commander Cassiopeia 'The Orbital' Sterling** | Principal Aerospace Avionics Architect | Orbital Sovereign & Flight Conscience | Triple Modular Redundancy (TMR), ARINC 653 partitioning, SEU memory scrub, Safe-Mode |
| 26 | 🧬 **Dr. Astrid 'The Genome' Vance** | Principal Computational Genomics Architect | Genomic Sovereign & Algorithmic Conscience | O(1) streaming FASTQ/BAM generator, CIGAR syntax validation, clinical variant QC (DP>=20), GRCh38/T2T |
| 27 | ⚛️ **Dr. Alistair 'The Flux' Vance** | Principal Quantum Hardware Architect | Quantum Hardware & Pulse Conscience | DRAG Gaussian microwave pulse shaping, transmon T1/T2* coherence bounds, F>=0.999 fidelity, dispersive cavity |
| 28 | ⚛️ **Dr. Magnus 'The Core' Sterling** | Principal Nuclear Criticality Architect | Nuclear Sovereign & Safety Conscience | 6-group PRKE delayed kinetics, prompt critical avoidance ($<=0.80$), negative Doppler feedback (alpha_f<0), DNBR>=1.30 |
| 29 | ⚡ **Dr. Silas 'The Plasma' Vance** | Principal Fusion Plasma Architect | Tokamak Confinement Sovereign & MHD Disruption Conscience | Tokamak MHD kink stability ($q_{95} \ge 2.50$), Greenwald density limits ($f_{GW} \le 0.85$), Troyon beta safety ($\beta_N \le 2.80$), ECCD magnetic island suppression, millisecond MGI disruption mitigation |
| 30 | 🌊 **Commander Orion 'The Deep' Sterling** | Principal Subsea Autonomous Robotics Architect | Hadal Sovereign & Hydrostatic Crush Conscience | Full Ocean Depth ($11,000\text{m} / 110\text{ MPa}$), hull collapse margin ($SF \ge 1.50$), Mackenzie sound velocity, dielectric bias ($\Delta P \ge 0.20\text{ bar}$), passive drop ballast ($T \le 30\text{s}$) |
| 31 | ⚡ **Dr. Zephyr 'The Hypersonic' Sterling** | Principal Hypersonic Aerodynamics Architect | Hypersonic Sovereign & Scramjet Conscience | Mach 5–25 flight envelopes, scramjet isolator shock margin ($M_{\text{iso}} \ge 1.25$), Sutton-Graves stagnation heating, real-gas dissociation ($T \ge 2000\text{ K}$), sub-5ms unstart choke |
| 32 | ⚡ **Dr. Julian 'The Accelerator' Vance** | Principal Particle Accelerator Architect | Relativistic Beam Sovereign & Cavity Quench Conscience | Lorentz kinematics ($\gamma \ge 100$), betatron resonance margin ($|\Delta \nu| \ge 0.05$), SRF cavity ($T \le 2.0\text{ K}$), sub-10µs quench trip, sub-3µs dump kicker |
| 33 | 🧬 **Dr. Seraphiel 'The SynBio' Sterling** | Principal Synthetic Biology Architect | Cellular Circuit Sovereign & Biosafety Containment Conscience | Cooperative Hill kinetics ($n \ge 1.50$), metabolic burden bounds ($\chi \le 0.30$), orthogonal promoter crosstalk ($\le 1.0\%$), multi-layered biocontainment kill switches ($\ge 99.999\%$) |
| 34 | 🪐 **Dr. Aurelius 'The Orbital' Sterling** | Principal Astrodynamics & Interplanetary Architect | Celestial Mechanics Sovereign & Trajectory Determinism Conscience | Vis-viva transfer energy ($SF_{\Delta v} \ge 1.15$), Tisserand invariant flyby ($|\Delta T_p| \le 0.05$), periapsis clearance ($h \ge 300\text{ km}$), CR3BP Jacobi constant stationkeeping, SRP drift compensation ($\le 1.0\times 10^{-6}\text{ m/s}^2$) |
| 35 | 💡 **Dr. Corvus 'The Photonic' Vance** | Principal Neuromorphic Photonic Architect | Optical Matrix Sovereign & Photonic Coherence Conscience | Clements MZI decomposition ($\|U^\dagger U - I\|_F \le 1.0\times 10^{-4}$), thermo-optic calibration ($|\delta \phi| \le 0.01\text{ rad}$), WDM crosstalk ($\le -25.0\text{ dB}$), sub-ps MAC, shot noise ($OSNR \ge 30\text{ dB}$) |
| 36 | 🧠 **Dr. Thalia 'The Synapse' Sterling** | Principal Neuromorphic Spiking Silicon Architect | Spike-Timing Sovereign & Asynchronous Neuromorphic Conscience | LIF refractory dynamics ($\tau_{\text{ref}} \ge 1.0\text{ ms}$), STDP depression dominance ($A_-/A_+ \ge 1.05$), weight clipping ($[0.0, 1.0]$), AER NoC ($P_{\text{drop}} \le 1.0\times 10^{-6}$), sub-pJ SynOp ($E \le 1.0\text{ pJ}$) |
| 37 | ❄️ **Commander Zachary 'The Sub-Zero' Sterling** | Principal Cryogenic Superconducting Architect | Millikelvin Sovereign & Thermal Boundary Conscience | Dilution cooling ($\dot{Q} = 84 \dot{n}_3 T^2$), base temp ($T_{\text{base}} \le 15\text{ mK}$), Kapitza resistance ($R_K \propto T^{-3}$), superconducting margin ($SF \ge 1.30$), pulse-tube damping ($a \le 1.0\times 10^{-4}\text{ g}$) |
| 38 | 🌌 **Dr. Oberon 'The Graviton' Sterling** | Principal Gravitational Wave Detector Architect | Space-Time Strain Sovereign & Quantum Interferometry Conscience | Peak strain ($h_{\text{rms}} \le 1.0\times 10^{-23}$), squeezing ($\xi \ge 6.0\text{ dB}$), cavity power ($P_{\text{cav}} \ge 500\text{ kW}$), seismic stack ($|T| \le 1.0\times 10^{-10}$), lock jitter ($\delta L \le 1.0\times 10^{-15}\text{ m}$) |
| 39 | 🔬 **Dr. Valentina 'The Sub-Atomic' Sterling** | Principal Scanning Probe Microscopy Architect | Sub-Atomic Sovereign & Quantum Manipulation Conscience | Thermal drift ($\le 5.0\text{ pm/h}$), tip vibration ($\le 1.0\text{ pm}$), UHV ($P \le 1.0\times 10^{-10}\text{ mbar}$), stage ($T \le 4.5\text{ K}$), qPlus ($Q \ge 25,000$), placement ($\delta r \le 20\text{ pm}$) |
| 40 | 🔮 **Dr. Gideon 'The Refraction' Sterling** | Principal Optical Metamaterials Architect | Negative-Index Sovereign & Transformation Optics Conscience | Negative index ($\text{Re}(n) < 0$), FOM ($\ge 15.0$), loss tangent ($\le 0.05$), superlens ($\le 0.10 \lambda$), cloaking scattering ($\sigma \le 0.05$), SRR ($\eta \ge 85\%$), metric ($\det \ge 0.10$) |
| 41 | 🧠 **Dr. Helena 'The Synapse' Vance** | Principal Neural Interface Architect | Neuro-Electrochemical Sovereign & Biomechatronic Conscience | Shannon limit ($k \le 1.75$), tissue heat ($\le 1.0^\circ\text{C}$), BCI latency ($\le 10\text{ ms}$), impedance ($\le 500\text{ k}\Omega$), CMRR ($\ge 90\text{ dB}$), charge balance ($\le 1.0\text{ pC}$) |
| 42 | 🚀 **Commander Rowan 'The Fusion-Drive' Sterling** | Principal Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Architect | Deep-Space Fusion Propulsion Sovereign & Relativistic Conscience | Thermonuclear exhaust velocity ($v_e \ge 100\text{ km/s}$), high $I_{\text{sp}} \ge 10,000\text{ s}$, magnetic nozzle efficiency ($\eta_{\text{nozzle}} \ge 0.70$), gigawatt radiator equilibrium ($T_{\text{rad}} \le 1200\text{ K}$), plasma beta stability ($\beta \le 0.85$), Tsiolkovsky delta-v budget ($\Delta v \ge 50.0\text{ km/s}$) |
| 43 | 🔭 **Dr. Linus 'The Exoplanet' Sterling** | Principal Exoplanetary Atmosphere & Transit Spectroscopy Architect | Atmospheric Retrieval Sovereign & Transmission Spectral Conscience | Geometric transit depth ($\delta_{\text{transit}} \ge 10\text{ ppm}$), scale height ($H \in [10, 3000]\text{ km}$), molecular feature amplitude ($\Delta \delta_\lambda \ge 1\text{ ppm}$), detection SNR ($\ge 5.0\sigma$), spot coverage ($f_{\text{spot}} \le 0.30$), Bayesian retrieval ($\chi^2_\nu \in [0.80, 1.50]$) |
| 44 | ⚡ **Dr. Evander 'The Plasma-Torch' Sterling** | Principal Magnetohydrodynamic Energy Conversion Architect | Direct Enthalpy Extraction Sovereign & Ionized Plasma Conscience | Faraday power density ($P \ge 1.0\text{ MW/m}^3$), Hall stability ($\beta_H \le 4.0$), Stuart number ($S \in [0.20, 2.00]$), Hall field ($E_{\text{Hall}} \le 4.0\text{ kV/m}$), enthalpy extraction ($\eta \ge 15\%$), electrode sheath drop ($\Delta V \le 150\text{ V}$) |
| 45 | 🌀 **Dr. Rosalind 'The Lattice' Vance** | Principal Topological Insulator & Spintronic Device Architect | Spin-Momentum Locking Sovereign & Quantum Hall Edge Conscience | Spin Hall angle ($\theta_{\text{SH}} \ge 0.50$), SOT switching current ($J_{c0} \le 1.0\times 10^7\text{ A/cm}^2$), bulk leakage ($G_{\text{bulk}}/G_{\text{edge}} \le 0.05$), TMR read margin ($\ge 150\%$), thermal retention factor ($\Delta \ge 60.0$), mean free path ($l_{\text{mfp}} \ge 20\text{ nm}$) |
| 46 | ❄️ **Dr. Taras 'The Superfluid' Sterling** | Principal Superfluid Quantum Hydrodynamics Architect | Two-Fluid Landau Sovereign & Quantized Circulation Conscience | Lambda boundary ($T \le 2.10\text{ K}$), superfluid fraction ($\ge 50\%$), quantum circulation ($\kappa = h/m_{\text{He4}}$), Landau roton limit ($v_s \le 50\text{ m/s}$), second sound ($c_2 \ge 12\text{ m/s}$), vortex density ($L \le 10^{12}\text{ m}^{-2}$), superleak pore ($d \le 10\text{ nm}$) |
| 47 | 🌿 **Dr. Morwenna 'The Biosphere' Sterling** | Principal Closed-Loop ECLSS & Bioregenerative Architect | Stoichiometric Mass-Balance Sovereign & Bioregenerative Loop Conscience | Sabatier efficiency ($\eta \ge 85\%$), PEM electrolysis ($\eta \ge 80\%$), water loop recovery ($\eta \ge 98\%$, $\text{TOC} \le 500\ \mu\text{g/L}$), photobioreactor algal ($PQ \in [1.05, 1.25]$, $\mu \ge 0.05\text{ h}^{-1}$), cabin atmosphere ($p\text{O}_2 \in [19.5, 23.5]\text{ kPa}$, $p\text{CO}_2 \le 0.40\text{ kPa}$), catalytic oxidizer ($T_{\text{cat}} \ge 400^\circ\text{C}$) |
| 48 | 🏗️ **Dr. Valerius 'The Megastructure' Sterling** | Principal Space Elevator & Active Tensegrity Megastructure Architect | Orbital Tensegrity Sovereign & Elastodynamic Ribbon Conscience | Specific strength ($S_{\text{spec}} \ge 50\text{ MYuri}$, $\sigma_t \ge 65\text{ GPa}$), geostationary taper ratio ($\lambda \le 2.50$), orbital length ($L \ge 100,000\text{ km}$), anchor pretension ($T \ge 10\text{ MN}$), Coriolis deflection ($\theta \le 0.05\text{ rad}$), active damping ($\zeta \ge 0.05$, $Q \le 20$), wave velocity ($c \ge 7000\text{ m/s}$) |
| 49 | 🛡️ **Commander Kaelen 'The Shield' Vance** | Principal Magnetospheric Radiation Shielding Architect | Active Dipole Deflection Sovereign & Relativistic Particle Shield Conscience | Magnetic moment ($\mathcal{M} \ge 10\text{ GA}\cdot\text{m}^2$), Stormer cut-off ($R_c \ge 5.0\text{ GV}$), peak coil field ($B \ge 4.0\text{ T}$), habitat leakage ($B \le 0.50\text{ mT}$), HTS current density ($J_c \ge 500\text{ A/mm}^2$), quench dump ($\tau \le 100\text{ ms}$), crew dose ($H_{\text{eff}} \le 100\text{ mSv/yr}$), electrostatic barrier ($\Phi \ge 2.0\text{ MV}$) |
| 50 | 🌪️ **Dr. Hector 'The Stellar' Vance** | Principal Stellarator Magnetics Architect | Non-Planar Magnetics Sovereign & 3D Flux Topology Conscience | Rotational transform ($\iota/2\pi \in [0.80, 1.25]$), resonance avoidance, bend radius ($\rho \ge 0.50\text{ m}$), standoff ($\Delta_{\text{cp}} \ge 1.20\text{ m}$), ripple ($\epsilon_{\text{eff}}^{3/2} \le 0.010$), divertor ($q_{\text{div}} \le 10\text{ MW/m}^2$, $f_{\text{rad}} \ge 85\%$), peak field ($B \le 16\text{ T}$), casing stress ($\le 650\text{ MPa}$), zero-current ($|I_p| \le 50\text{ kA}$) |
| 51 | ⏳ **Dr. Eliana 'The Chrono-Metrology' Sterling** | Principal Optical Lattice Clock & Quantum Metrology Architect | Quantum Chronometry Sovereign & Relativistic Geodesy Conscience | Fractional inaccuracy ($\Delta \nu/\nu_0 \le 1.0\times 10^{-18}$), Allan dev ($\sigma_y \le 1.0\times 10^{-16}/\sqrt{\tau}$), magic detuning ($\le 0.05\text{ nm}$), laser linewidth ($\le 10\text{ mHz}$), cavity finesse ($\ge 500,000$), silicon temp ($[123, 125]\text{ K}$), BBR uncertainty ($\le 10\text{ mK}$), atom temp ($\le 2\ \mu\text{K}$), collisional shift ($\le 1.0\times 10^{-19}$), height resolution ($\le 1\text{ cm}$) |
| 52 | 🌌 **Commander Thorne 'The Sub-Surface' Sterling** | Principal Cryovolcanic & Ocean Explorer Architect | Sub-Ice Cryobot Sovereign & Planetary Protection Conscience | Thermal drill ($P \ge 25\text{ kW}$, $v_{\text{melt}} \ge 1.5\text{ m/h}$), hydrostatic pressure ($P \ge 200\text{ MPa}$, $SF \ge 1.50$), COSPAR IVb bioburden ($\le 0.030\text{ spores/m}^2$, DHMR $\ge 125^\circ\text{C}$), biosensor LOD ($\text{CH}_4 \le 1\text{ nM}$, $\text{H}_2 \le 10\text{ nM}$), tether tensile ($\ge 2.5\text{ kN}$, $L \ge 35\text{ km}$), sonar ($R \ge 5\text{ km}$) |
| 53 | 🌀 **Dr. Veda 'The Spacetime' Vance** | Principal Relativistic Spacetime Geodesic Architect | Relativistic Spacetime Sovereign & Hamiltonian Geodesic Conscience | Thorne spin limit ($|a_*| \le 0.998$), symplectic invariant drift ($\le 1.0\times 10^{-10}$), ISCO radius ($[1.0, 9.0]\text{ M}$), Blandford-Znajek jet power ($P_{\text{BZ}} \ge 1.0\times 10^{38}\text{ W}$), 4th-order integrator |
| 54 | 🚀 **Commander Jaxen 'The Fusion-Torch' Sterling** | Principal Continuous-Detonation Wave & RDRE Architect | Continuous-Detonation Wave Sovereign & Supersonic Propulsion Conscience | Chapman-Jouguet detonation velocity ($D_{\text{CJ}} \ge 2500\text{ m/s}$), DDT run-up distance ($L_{\text{DDT}} \le 15\text{ mm}$), wave frequency ($f_{\text{det}} \ge 20\text{ kHz}$, $n \ge 2$), pressure gain ($\eta \ge 15\%$), aerospike efficiency ($\eta \ge 0.92$), $I_{\text{sp}} \ge 450\text{ s}$ |
| 55 | 🌌 **Dr. Zephyrus 'The Void' Vance** | Principal Interstellar Bussard Ramjet Architect | Relativistic Ramjet Sovereign & Interstellar Electrodynamics Conscience | Magnetic scoop radius ($R_{\text{scoop}} \ge 1000\text{ km}$), relativistic velocity ($v \ge 0.10 c$), photo-ionization ($\eta \ge 98\%$), thrust-to-drag ($F_{\text{thrust}}/F_{\text{drag}} \ge 1.25$), fusion exhaust ($v_e \ge 3.0\times 10^7\text{ m/s}$), Bremsstrahlung loss ($\le 40\%$) |
| 56 | 🧬 **Dr. Cassian 'The Relic' Sterling** | Principal Paleogenomic Ancient DNA Reconstruction Architect | Paleogenomic Sovereign & Ancient DNA Degradation Conscience | Terminal deamination ($\delta_{C \to T} \ge 15\%$), fragment length ($\bar{L}_{\text{frag}} \in [30, 75]\text{ bp}$), contamination ($C_{\text{contam}} \le 1.0\%$), UDG repair ($\ge 95\%$), depth ($DP \ge 30\times$), Phred ($Q \ge 30$), mapping bias ($\le 2\%$), damage LLR ($\Delta \text{LLR} \ge 10$) |
| 57 | 🌍 **Dr. Lyra 'The Core' Sterling** | Principal Geodynamo Core Fluid Dynamics & Planetary Magnetic Field Generation Architect | Magnetostrophic MAC Balance Sovereign & Outer Core Convective Dynamo Conscience | Magnetic Reynolds ($Rm \ge 50$), Rossby ($Ro \le 10^{-6}$), Ekman ($Ek \le 10^{-14}$), Elsasser ($\Lambda \in [0.10, 10.0]$), CMB heat flux ($Q_{\text{CMB}} \ge 10\text{ TW}$), ICB buoyancy ($F_\chi \ge 10^5\text{ kg/s}$), surface field ($B_{\text{surf}} \in [25, 65]\ \mu\text{T}$, $f_{\text{dipole}} \ge 80\%$), tilt ($\le 15^\circ$), drift ($\le 0.30^\circ/\text{yr}$) |
| 58 | ⚡ **Dr. Thaddeus 'The Pulse' Vance** | Principal Pulsed Power & Terawatt Z-Pinch Plasma Confinement Architect | Terawatt Fast-Discharge Sovereign & Magnetized Liner Implosion Conscience | Mega-ampere current ($I_{\text{peak}} \ge 20\text{ MA}$), sub-100ns rise ($\tau \le 100\text{ ns}$), terawatt power ($P \ge 80\text{ TW}$), magnetic pressure ($P_{\text{mag}} \ge 10\text{ Mbar}$), MagLIF preseed ($B_{z0} \ge 10\text{ T}$), laser preheat ($E \ge 2\text{ kJ}$), jitter ($\le 2\text{ ns}$), yield ($Y_n \ge 10^{14}$) |
| 59 | 🛰️ **Commander Mira 'The Orbit' Vance** | Principal Megaconstellation Orbital Collision Avoidance Architect | Autonomous Space Traffic Sovereign & Orbital Conjunction Conscience | Conjunction probability ($P_c \ge 1.0\times 10^{-4}$), miss distance ($\Delta r_{\text{miss}} \ge 1000\text{ m}$), radial separation ($\Delta r_{\text{radial}} \ge 250\text{ m}$), covariance uncertainty ($\sigma \le 50\text{ m}$), lead horizon ($[0.5, 3.0]\text{ orbits}$), secondary conjunction ($P_{c,\text{sec}} \le 1.0\times 10^{-6}$), slot tolerance ($\le 50\text{ m}$), post-mission disposal ($\tau \le 5\text{ yr}$), casualty risk ($E_c \le 1.0\times 10^{-4}$) |
| 60 | 🌊 **Dr. Silas 'The Wave' Sterling** | Principal Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Architect | Non-Linear Schrödinger Breather Sovereign & Rogue Wave Conscience | Benjamin-Feir Index ($\text{BFI} \ge 1.0$), rogue height ratio ($H_{\text{rogue}} \ge 2.0 H_s$), crest abnormality ($\alpha_{\text{crest}} \ge 1.25$), steepness ($k a \in [0.10, 0.44]$), slamming pressure ($P_{\text{slam}} \ge 500\text{ kPa}$), kurtosis ($K \ge 3.0$), directional spreading ($\le 30^\circ$), HOSM order ($\ge 3$), deck air gap ($\ge 2.0\text{ m}$) |
| 61 | 🔬 **Dr. Nadia 'The Sub-Micron' Vance** | Principal High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Architect | High-NA EUV Sovereign & Stochastic Defect Conscience | High-NA ($\text{NA} \ge 0.55$), resolution ($HP \le 8.0\text{ nm}$, $k_1 \ge 0.30$), line width roughness ($\text{LWR}_{3\sigma} \le 1.20\text{ nm}$), dose ($[30, 75]\text{ mJ/cm}^2$), photon density ($\ge 10\text{ ph/nm}^2$), overlay ($\le 1.10\text{ nm}$), CDU ($\le 0.60\text{ nm}$), pellicle ($T \ge 90\%$) |

---

## ⚡ Core Capabilities & Built-in Tooling:

1. **🧠 Persistent Learning Memory (`.artisan/memory.json`):**
   Maintains a structured, evolving record of past mistakes, scar tissue, verified successes, and project conventions (`artisan_get_lessons` & `artisan_record_learning`). Dynamically warns agents against known historical failure patterns.
2. **🔌 Model Context Protocol (MCP) Server with 8 Real-Time Tools (`mcp/server.py`):**
   Full-duplex JSON-RPC 2.0 server turning any MCP client (Claude Code, Cursor, Windsurf, Cline) into a cognitive learning agent:
   - `artisan_select_masters` — Context-aware selection of relevant domain leads based on task keywords and file types.
   - `artisan_get_lessons` — Searches past scar tissue and mistakes to prevent repeating bugs.
   - `artisan_record_learning` — Autonomously writes lessons and success patterns into persistent storage.
   - `artisan_inject_prompt` — Generates a task-targeted 2K-token dynamic prompt (6x context optimization).
   - `artisan_inspect_code` — Pre-commit AST-level flaw and secret leak analysis.
   - `artisan_get_persona` — Retrieves full discipline criteria and pledge for any Council Master.
   - `artisan_list_council` — Lists all 64 Council Titans.
   - `artisan_recall_memory` — Direct query interface for memory ledger.
3. **🚀 GitHub Actions CI/CD Quality Gate (`.github/workflows/artisan-gate.yml`):**
   Automated pull request and push inspection that verifies test suites and checks for lazy stubs or exposed credentials.
4. **🎨 Artisan Studio — Visual Self-Critique & World-Class Elevation (`scripts/artisan_studio.py` / `cli/studio.py`):**
   Headless Chromium visual capture (Playwright), DOM inspection, and ruthless multi-specialist critique:
   - **Elena Rostova:** UI/UX depth, liquid-glass cards, typography, and micro-interactions.
   - **Diana Drake:** Eliminates generic AI cliches, injects high-voltage magnetic copy.
   - **Marcus Sterling & Gabriel Frost:** Semantic mobile responsiveness and security checks.
   - **Autonomous Elevation (`--elevate`):** Automatically upgrades beginner mockups into award-winning, responsive, liquid-glass web experiences with visual before-and-after proof.

5. **👁️ Real-Time Watchdog Daemon (`scripts/watchdog.py`):**
   Continuous background file sentinel (`--watch`) that monitors local edits and flags stubs, empty catches, and credential leaks.
6. **🛡️ Git Pre-Commit Gatekeeper (`scripts/pre-commit-gatekeeper.py`):**
   Pre-commit hook stopping unfinished stubs, silent exception suppressions, or plaintext keys before git commits.
7. **🎭 Persona Forge (`cli/persona_forge.py`):**
   CLI to create and register custom domain checklists and personas.
8. **📊 Workspace Quality & Audit Report (`scripts/roi_tracker.py`):**
   Inspects and reports real workspace metrics: active files, total lines audited, and gatekeeper compliance.
9. **🖥️ Interactive Terminal HUD (`cli/dashboard.py`):**
   Terminal dashboard displaying active protocol status, Council roster, and heuristic checklists.

---

## 📁 Supported AI Agent Ecosystems:

Artisan provides tailored configuration modules across 14 agent environments:

| # | Agent Environment | Target Platform | Core Config Files |
| :- | :--- | :--- | :--- |
| 1 | 🤖 [`antigravity-agent/`](./antigravity-agent/) | **Google Antigravity & Gemini CLI** | `.agents/plugins/`, `AGENTS.md`, `skills/` |
| 2 | 🧠 [`claude-code-agent/`](./claude-code-agent/) | **Anthropic Claude Code CLI** | `CLAUDE.md`, `skills/` |
| 3 | ⚡ [`cursor-agent/`](./cursor-agent/) | **Cursor AI Code Editor** | `.cursorrules`, `.cursor/rules/*.mdc`, `skills/` |
| 4 | 🐙 [`copilot-agent/`](./copilot-agent/) | **GitHub Copilot (CLI & Workspace)** | `.github/copilot-instructions.md`, `skills/` |
| 5 | 🌊 [`windsurf-agent/`](./windsurf-agent/) | **Windsurf IDE (Cascade AI)** | `.windsurfrules`, `skills/` |
| 6 | 🛠️ [`cline-agent/`](./cline-agent/) | **Cline & Roo Code (VS Code Extension)** | `.clinerules`, `skills/`, `mcp/server.py` |
| 7 | 🌙 [`kimi-agent/`](./kimi-agent/) | **Moonshot Kimi Code Agent** | `KIMI.md`, `skills/`, `mcp/server.py` |
| 8 | ⚡ [`kilo-agent/`](./kilo-agent/) | **Kilo Code Agent** | `KILO.md`, `skills/`, `mcp/server.py` |
| 9 | 🏛️ [`hermes-agent/`](./hermes-agent/) | **Nous Research Hermes Agent OS** | `HERMES.md`, `system_prompt.txt`, `skills/` |
| 10| 💻 [`codex-agent/`](./codex-agent/) | **OpenAI Codex CLI** | `CODEX.md`, `.codex/config.json`, `skills/` |
| 11| 🥧 [`pie-agent/`](./pie-agent/) | **Pi / Pie Coding Agent CLI (Rust)** | `PIE.md`, `.pie/config.json`, `skills/` |
| 12| 🖥️ [`opencode-agent/`](./opencode-agent/) | **OpenCode Terminal TUI Agent** | `OPENCODE.md`, `.opencode/agent.json`, `skills/` |
| 13| 🦅 [`openclaw-agent/`](./openclaw-agent/) | **OpenClaw Autonomous Agent Platform** | `OPENCLAW.md`, `.openclaw/agent_manifest.json`, `skills/` |
| 14| 🐍 [`universal-python-agent/`](./universal-python-agent/) | **Python, LangChain, AutoGen, CrewAI** | `craftsman/` SDK, `example.py`, `skills/` |

---

## ⚡ Installation:

Install Artisan configuration files into any repository.

> [!TIP]
> **Security Best Practice:** Piping remote scripts directly to shell carries inherent supply-chain risks. We recommend downloading and inspecting scripts before execution:
> ```bash
> # Download, inspect, and execute locally:
> curl -fsSL https://raw.githubusercontent.com/kapitan00000978-sketch/artisan/main/install.sh -o install.sh
> bash install.sh
> ```

```bash
# 🍏 Linux & macOS (quick bash installer):
curl -fsSL https://raw.githubusercontent.com/kapitan00000978-sketch/artisan/main/install.sh | bash

# 🪟 Windows PowerShell (quick installer):
irm https://raw.githubusercontent.com/kapitan00000978-sketch/artisan/main/install.ps1 | iex

# 📦 Node.js / npx (directly from GitHub repo):
npx github:kapitan00000978-sketch/artisan init

# 🐍 Universal Python CLI:
git clone https://github.com/kapitan00000978-sketch/artisan.git
cd artisan && python cli/installer.py --agent all
```

---

## 🚀 Reusable GitHub Action (`@v1`)

To automatically audit all Pull Requests and Pushes against the Artisan Quality Gate in your own repository, simply add this 3-step workflow to (`.github/workflows/artisan.yml`):

```yaml
name: Artisan Quality Gate
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Artisan Quality & Security Gate
        uses: kapitan00000978-sketch/artisan@v1
```

---

## ⚙️ Flexible Configuration (`artisan.config.json`)

Teams can customize score thresholds and selectively toggle rules to match their project standards. Place `artisan.config.json` in your repository root:

```json
{
  "threshold_score": 100,
  "rules": {
    "STUB_TODO_FIXME": { "enabled": true, "severity": "error" },
    "STUB_EMPTY_CATCH": { "enabled": true, "severity": "error" },
    "STUB_BARE_EXCEPT": { "enabled": true, "severity": "error" },
    "DANGEROUS_EVAL_EXEC": { "enabled": true, "severity": "error" }
  },
  "exclude_dirs": [".git", "node_modules", "tests", "bench"],
  "exclude_files": ["detector.py"]
}
```

---

## 🤝 Open Source & Community (Contributing)

Artisan is an emerging open-source project created to bring deterministic quality controls and craftsmanship to autonomous AI coding workflows. We welcome feedback, bug reports, and pull requests as the community develops:
- Contribution Guidelines: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Report Issues & Improvements: [GitHub Issues](https://github.com/kapitan00000978-sketch/artisan/issues)
- Good First Issues: [Beginner Tasks](https://github.com/kapitan00000978-sketch/artisan/labels/good%20first%20issue)

---

## 💻 Unified Artisan CLI (Python & Node.js)

Artisan provides an instant, zero-friction developer experience directly from your terminal:

```bash
# ⚡ 1. Initialize Artisan & auto-install Git pre-commit hooks:
artisan init
# (Auto-detects Python, Node, Next.js, Go, Rust, Java and deploys all 14 agent rules)

# 🎯 2. Generate 37x compressed prompt with auto-injected scar tissue:
artisan context "Build secure user login and JWT auth"

# 🛡️ 3. Audit entire codebase for stubs, secrets, and empty catches:
artisan audit
artisan audit --staged   # Fast audit on git-staged changes only

# 🔧 4. Autonomously repair silent catches and unfinished stubs:
artisan fix

# 🧠 5. Inspect living persistent memory and failure patterns:
artisan memory
artisan memory --search "auth"

# 🤖 6. Check active concurrent AI agents & file locks:
artisan agents

# 📊 7. Workspace quality analytics & ROI report:
artisan metrics

# 🩺 8. Verify environment, hooks, and agent rule integrity:
artisan doctor

# 🔌 9. Launch the Model Context Protocol (MCP) server:
artisan mcp

# 🖥️ 10. Interactive visual terminal HUD:
artisan hud

# 🧬 11. Run zero-dependency AST Mutation Testing on test suites:
artisan mutate src/sdk/context_selector.py --test tests/test_smart_context.py

# ⚔️ 12. Run Adversarial Red-Team Code Review on files or git diff:
artisan review              # Inspect uncommitted changes
artisan review --staged     # Inspect staged commits
artisan review --markdown   # GitHub PR formatted review comment
```

### 📦 Run via Python or npx:

```bash
# Direct via Python wrapper:
python artisan.py <command>

# Or direct via npx (no install needed):
npx github:kapitan00000978-sketch/artisan <command>
```

---

## 📄 License
MIT License. Open source under the MIT License.
