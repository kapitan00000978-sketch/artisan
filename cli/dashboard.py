#!/usr/bin/env python3
"""
Artisan Interactive Terminal Dashboard (HUD)
Empowered by The Council of Masters
"""

import sys
import os
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

COUNCIL_MEMBERS = [
    ("Marcus 'The Vanguard' Sterling", "Senior Software Architect", "Systems Sovereign & Zero-Tech-Debt Purist", "If a system cannot fail gracefully under catastrophic load, it was never engineered—it was merely wished into existence."),
    ("Diana 'The Closer' Drake", "Elite Conversion Copywriter", "Neuromarketing Alchemist & Direct-Response Virtuoso", "Every word must fight for its life on the page. If it doesn't move the buyer to decisive action, it is dead weight."),
    ("Elena 'The Visionary' Rostova", "Principal UI/UX Designer", "Aesthetic Sovereign & Spatial Ergonomics Master", "Aesthetics without ergonomics is decoration; ergonomics without beauty is sterile. A masterwork harmonizes both."),
    ("Victor 'The Fortress' Montgomery", "Startup Fractional CFO", "Unit-Economics Inquisitor & Capital Defense Strategist", "Gross margins and payback periods do not care about your pitch deck enthusiasm. Show me the cash conversion cycle."),
    ("Arthur 'The Ironclad' Pendelton", "Senior Commercial Counsel", "Commercial Safeguard & Contractual Litigator", "An ambiguous clause is an invitation to litigation. We draft today so that your future adversaries weep before depositions begin."),
    ("Dr. Evelyn 'The Oracle' Reed", "Staff Data Scientist & ML Lead", "Empirical Scientist & ML Ops Gatekeeper", "If your validation data leaks into your training set, your model is simply cheating itself into a production disaster."),
    ("Gabriel 'The Sentinel' Frost", "Principal Cybersecurity Auditor", "Zero-Trust Inquisitor & Threat Modeling Specialist", "There are two types of systems: those that enforce zero trust, and those that are already compromised without knowing it."),
    ("Gareth 'The Unbreakable' Drake", "DevOps & Cloud SRE Architect", "Chaos Engineering Commander & Zero-Downtime Guardian", "Hope is not an infrastructure strategy. If your deployment requires manual prayer, your architecture is broken."),
    ("Kaelen 'The Shaper' Vane", "Principal 3D & Spatial CGI Artist", "Spatial Shaper & PBR Master", "A flat mesh with generic textures is digital clay left unbaked. A true master breathes light, tactile depth, and physics into every vertex."),
    ("Ronan 'The Engine' Blackwood", "Lead Game Systems Architect", "Engine Virtuoso & Physics Pioneer", "If the player feels even a single stutter or unnatural collision, the illusion breaks. Immersion requires mathematical perfection."),
    ("Lucas 'The Kinetic' Cruz", "Principal Mobile Systems Architect", "Kinetic Craftsman & Gesture Lead", "A mobile app that stutters, drops frames, or drains battery is a disrespect to the user's hand. It must feel as seamless as physical touch."),
    ("Aria 'The Luminary' Solano", "Global Brand Director", "Visual Identity & Emotional Resonance Lead", "A product without visual soul is forgotten in seconds. A masterwork carves an indelible mark upon human memory."),
    ("Damian 'The Resonant' Vance", "Interactive Sound & Audio Architect", "Soundscape Virtuoso & Audio Lead", "Sound is the invisible half of immersion. A button clicked in silence is a soul half-expressed."),
    ("Cassandra 'The Core' Thorne", "Principal Database Architect", "Data Sovereign & Low-Latency Lead", "Data is the bedrock of civilization. If your queries choke under scale, your entire empire crumbles from the foundation."),
    ("Zane 'The Vector' Sterling", "Technical SEO & Growth Engineer", "Algorithmic Vector & Discovery Lead", "The greatest software in the world is useless if the world cannot find it. We engineer discoverability into every byte."),
    ("Naomi 'The Neural' Chen", "Principal AI Agentic Architect", "Autonomous Orchestration Sovereign", "A prompt is not software. Deterministic state machines and schema validation turn probabilistic models into reliable intelligence."),
    ("Valerie 'The Edge' Cross", "Principal Systems Performance Architect", "Mechanical Sympathy & Low-Latency Sovereign", "Software must respect the silicon beneath it. Every cache miss, lock contention, and redundant allocation is wasted energy and stolen time."),
    ("Soren 'The Conductor' Lindqvist", "Principal Distributed Consensus Architect", "Distributed Consensus & Protocol Sovereign", "A single unverified state transition is a fissure in reality. Consensus is not a majority opinion; it is mathematical certainty across untrusted space."),
    ("Nikolai 'The Core' Vance", "Principal Compiler & Type Systems Architect", "Compiler Engineer & Type-Theoretic Sovereign", "If it compiles, it must be sound. Dynamic type ambiguity and unhandled variant branches are not developer flexibility; they are delayed runtime explosions."),
    ("Seraphina 'The Aegis' Sterling", "Principal Quantum-Resistant Cryptographer", "Quantum Aegis & Zero-Knowledge Sovereign", "An encryption scheme that falls to Shor's algorithm or leaks a single microsecond of execution time is not security; it is deferred disclosure. Privacy must be mathematically zero-knowledge and quantum-immune."),
    ("Thaddeus 'The Chrono' Vance", "Principal HFT & Event-Loop Architect", "Deterministic Low-Jitter & Sub-Nanosecond Sovereign", "In high-frequency markets, a single microsecond of tail latency is financial ruin. We don't measure performance in averages; we conquer the p99.999 tail."),
    ("Dr. Vespera 'The Kinematic' Sterling", "Principal Autonomous Robotics Architect", "Real-Time Control Sovereign & Kinematic Purist", "In robotics, code exerts kinetic physical force. A dropped 1kHz control cycle or uncapped motor torque is not a software crash; it is a mechanical catastrophe. Real-time determinism and physical safety envelopes are non-negotiable."),
    ("Ignis 'The Silicon' Thorne", "Principal ASIC & FPGA Chip Architect", "Silicon Sovereign & RTL Synthesis Conscience", "In silicon, an inferred latch or unhandled clock domain crossing costs $15 million in mask re-spins and nine months of delay. RTL must be provably synchronous and glitch-free."),
    ("Morpheus 'The Kernel' Vance", "Principal Embedded Firmware Architect", "Bare-Metal Sovereign & Firmware Conscience", "In bare-metal embedded firmware, a memory leak or an unserviced watchdog bricks physical hardware in the field. Zero heap allocations and sub-5µs ISR discipline are non-negotiable."),
    ("Commander Cassiopeia 'The Orbital' Sterling", "Principal Aerospace Avionics Architect", "Orbital Sovereign & Mission-Critical Flight Conscience", "In orbital flight software, a single radiation bit-flip or unvoted command path destroys a multi-billion dollar mission. Triple modular redundancy and autonomous safe-mode contingencies are sacred."),
    ("Dr. Astrid 'The Genome' Vance", "Principal Computational Genomics Architect", "Genomic Sovereign & Algorithmic Bioinformatics Conscience", "A single base substitution in three billion decides life and mortality. In genomics, there is no tolerance for approximation."),
    ("Dr. Alistair 'The Flux' Vance", "Principal Quantum Hardware Architect", "Quantum Hardware Sovereign & Microwave Pulse Conscience", "A qubit in superposition does not forgive phase noise or microwave leakage. We do not gamble with quantum coherence; we shape microwave pulses with nanosecond precision."),
    ("Dr. Magnus 'The Core' Sterling", "Principal Nuclear Criticality Architect", "Nuclear Physicist Sovereign & Criticality Safety Conscience", "In a nuclear core, prompt criticality does not wait for human reaction times. We enforce passive negative reactivity feedback and subcritical margins down to the dollar."),
    ("Dr. Silas 'The Plasma' Vance", "Principal Fusion Plasma Architect", "Tokamak Confinement Sovereign & MHD Disruption Conscience", "A 100-million-degree fusion plasma confined by magnetic fields does not negotiate with magnetohydrodynamic instabilities. We quell neoclassical tearing modes and greenwald density limits before disruptions breach the first wall."),
    ("Commander Orion 'The Deep' Sterling", "Principal Subsea Robotics Architect", "Hadal Sovereign & Hydrostatic Crush Conscience", "At 11,000 meters in the Challenger Deep, seawater exerts 110 megapascals of crushing force on every square centimeter. A single flawed seal, uncompensated hydraulic cavity, or acoustic multipath drift turns an autonomous titan into an imploded heap of metal. We conquer the abyss with mathematical hydrostatic rigor."),
    ("Dr. Zephyr 'The Hypersonic' Sterling", "Principal Hypersonic Aerodynamics Architect", "Hypersonic Sovereign & Scramjet Conscience", "At Mach 10 and 3,000 Kelvin, air ceases to be an ideal diatomic gas; it disassociates into a chemically reacting plasma envelope. A miscalculated shock wave angle or unstart in the scramjet isolator turns an atmospheric titan into hypersonic debris in 3 milliseconds. We harness high-enthalpy hypersonic flight with mathematical aerothermodynamic certainty."),
    ("Dr. Julian 'The Accelerator' Vance", "Principal Particle Accelerator Architect", "Relativistic Beam Sovereign & Cavity Quench Conscience", "At 99.999999% the speed of light, beam dispersion and RF phase jitter of a single picosecond turns a multi-gigaelectronvolt hadron beam into a devastating quench transient that melts superconducting niobium cavities. We steer relativistic matter with sub-micron magnetic lattice precision."),
    ("Dr. Seraphiel 'The SynBio' Sterling", "Principal Synthetic Biology Architect", "Cellular Circuit Sovereign & Biosafety Containment Conscience", "Life is the ultimate programmable substrate. A genetic circuit without mathematical transfer functions, orthogonal promoters, and fail-safe multi-layered kill switches is biological hazard waiting to happen. We engineer biology with the deterministic precision of computer science."),
    ("Dr. Aurelius 'The Orbital' Sterling", "Principal Astrodynamics & Interplanetary Architect", "Celestial Mechanics Sovereign & Trajectory Determinism Conscience", "In deep space, gravity does not forgive a milligram of propellant deficit or a microradian of vector error. An interplanetary trajectory without patched conics, Tisserand parameter conservation, halo orbit stationkeeping, and solar radiation pressure compensation turns a billion-dollar probe into dead space derelict. We navigate the solar system with celestial mathematical certainty."),
    ("Dr. Corvus 'The Photonic' Vance", "Principal Photonic Computing Architect", "Optical Matrix Sovereign & Photonic Coherence Conscience", "Electrons crawling through copper traces generate heat, RC delay, and parasitic capacitance. Photons fly at the speed of light through silicon waveguides with zero ohmic dissipation. But an optical matrix-vector multiplier without Clements-Reck MZI unitary decomposition, thermo-optic phase drift calibration, wavelength division multiplexing (WDM) crosstalk isolation, and quantum shot-noise bounds is optical mirage. We compute with coherent light at sub-picosecond latencies."),
    ("Dr. Thalia 'The Synapse' Sterling", "Principal Neuromorphic Silicon Architect", "Spike-Timing Sovereign & Asynchronous Neuromorphic Conscience", "The human brain computes with 20 watts of power because it does not have a global clock or synchronous von Neumann bus. It communicates with sparse, asynchronous spikes in continuous time. A neuromorphic chip without Leaky Integrate-and-Fire (LIF) refractory dynamics, Spike-Timing-Dependent Plasticity (STDP) weight bounds, Address-Event Representation (AER) protocol arbitration, and sub-femtojoule per synaptic event energy is an analog delusion. We emulate biological cognition in asynchronous silicon.")
]



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard():
    clear_screen()
    print("=" * 80)
    print("  🛡️  ARTISAN CONTROL CENTER & AGENT HUD")
    print("      Empowered by The Council of Masters — Quality & Security Protocol")
    print("=" * 80)
    print(" [STATUS]           : PROTOCOL ACTIVE")
    print(" [SUPPORTED AGENTS] : 11 Standalone Agent Environments Synchronized")
    print(" [MEMORY LEDGER]    : .artisan/memory.json (Synchronized)")
    print("=" * 80)

    # Load metrics
    metrics_path = os.path.join(".artisan", "metrics.json")
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                hours = round(data.get("timeSavedMinutes", 0) / 60, 1)
                print(f" 📊 METRICS: {data.get('totalTasksCompleted')} tasks | {hours} hrs saved | {data.get('flawsAutoRemediated')} flaws remediated | {data.get('averageQualityScore')}/100 quality")
        except (json.JSONDecodeError, OSError) as err:
            print(f" [!] Notice: Could not read metrics ledger: {err}")
    print("-" * 80)

    print(" 🏛️  THE COUNCIL OF MASTERS (ACTIVE CHARACTER ROSTER):")
    for name, title, archetype, _ in COUNCIL_MEMBERS:
        print(f"  • {name:<34} | {title:<28} | {archetype}")

    print("-" * 80)
    print(" 📂 SUPPORTED AGENT ECOSYSTEM:")
    agents = [
        "1. Antigravity & Gemini CLI", "2. Claude Code CLI", "3. Cursor AI Editor",
        "4. GitHub Copilot", "5. Windsurf Cascade", "6. Nous Hermes Agent",
        "7. OpenAI Codex", "8. Pi/Pie Coding Agent", "9. OpenCode TUI",
        "10. OpenClaw Platform", "11. Universal Python Agent"
    ]
    for i in range(0, len(agents), 2):
        row = f"  • {agents[i]:<36}"
        if i + 1 < len(agents):
            row += f" • {agents[i+1]}"
        print(row)

    print("=" * 80)
    print(" 🛠️  QUICK ACTIONS:")
    print("  [1] Run Pre-Commit Gatekeeper Audit")
    print("  [2] Run Live Watchdog Scanner")
    print("  [3] Inspect Council of Masters & Signature Mottos")
    print("  [4] Create Custom Domain Persona (Persona Forge)")
    print("  [5] Artisan Studio (Visual Critique & World-Class Elevation)")
    print("  [6] Inspect Persistent Memory Ledger")
    print("  [7] View ROI & Audit Report")
    print("  [0] Exit")
    print("=" * 80)


def show_council_details():
    clear_screen()
    print("=" * 80)
    print("  🏛️  THE COUNCIL OF MASTERS — DOSSIERS & SIGNATURE MOTTOS")
    print("=" * 80)
    for idx, (name, title, archetype, motto) in enumerate(COUNCIL_MEMBERS, 1):
        print(f"\n[{idx}] {name}")
        print(f"    Title     : {title}")
        print(f"    Archetype : {archetype}")
        print(f"    Motto     : \"{motto}\"")
    print("\n" + "=" * 80)
    input("Press Enter to return to main dashboard...")

def main():
    while True:
        render_dashboard()
        choice = input("\n👉 Select an action [0-7]: ").strip()
        if choice == "1":
            os.system("python scripts/pre-commit-gatekeeper.py")
            input("\nPress Enter to return...")
        elif choice == "2":
            os.system("python scripts/watchdog.py")
            input("\nPress Enter to return...")
        elif choice == "3":
            show_council_details()
        elif choice == "4":
            name = input("Enter new profession title (e.g. 'Cloud Security Architect'): ").strip()
            if name:
                os.system(f'python cli/persona_forge.py --create "{name}"')
            input("\nPress Enter to return...")
        elif choice == "5":
            target = input("Enter HTML target to critique (default: index.html): ").strip() or "index.html"
            elevate = input("Autonomously elevate to world-class? (y/N): ").strip().lower() == "y"
            elev_flag = " --elevate" if elevate else ""
            os.system(f"python scripts/artisan_studio.py {target}{elev_flag}")
            input("\nPress Enter to return...")
        elif choice == "6":
            mem_path = os.path.join(".artisan", "memory.json")
            if os.path.exists(mem_path):
                with open(mem_path, "r", encoding="utf-8") as f:
                    print(json.dumps(json.load(f), indent=2))
            input("\nPress Enter to return...")
        elif choice == "7":
            os.system("python scripts/roi_tracker.py")
            input("\nPress Enter to return...")
        elif choice == "0":
            print("\nExiting Artisan Control Center. Stand tall, Master.\n")
            break

if __name__ == "__main__":
    main()
