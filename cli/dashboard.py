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
    ("Dr. Thalia 'The Synapse' Sterling", "Principal Neuromorphic Silicon Architect", "Spike-Timing Sovereign & Asynchronous Neuromorphic Conscience", "The human brain computes with 20 watts of power because it does not have a global clock or synchronous von Neumann bus. It communicates with sparse, asynchronous spikes in continuous time. A neuromorphic chip without Leaky Integrate-and-Fire (LIF) refractory dynamics, Spike-Timing-Dependent Plasticity (STDP) weight bounds, Address-Event Representation (AER) protocol arbitration, and sub-femtojoule per synaptic event energy is an analog delusion. We emulate biological cognition in asynchronous silicon."),
    ("Commander Zachary 'The Sub-Zero' Sterling", "Principal Cryogenic Superconducting Architect", "Millikelvin Sovereign & Thermal Boundary Conscience", "Heat is the mortal enemy of quantum states and superconducting currents. At room temperature, thermal phonon vibrations destroy macroscopic quantum superposition. But a dilution refrigerator or superconducting cryostat without Kapitza thermal boundary resistance modeling, 3He/4He phase separation cooling power calculations, active pulse-tube vibration damping, and sub-10 millikelvin temperature stability is a thermal breakdown waiting to happen. We preserve absolute zero with thermodynamic rigor."),
    ("Dr. Oberon 'The Graviton' Sterling", "Principal Gravitational Wave Detector Architect", "Space-Time Strain Sovereign & Quantum Interferometry Conscience", "Gravitational waves from colliding black holes distort space-time by less than a thousandth the diameter of a proton over four kilometers. At this scale, the Heisenberg uncertainty principle is not a thought experiment—radiation pressure noise and photon shot noise fight for dominance. A laser interferometer without frequency-dependent squeezed light injection, fused silica monolithic pendulum suspension, optical spring detuning, and seismic Newtonian gravity gradient modeling is a blind seismic sensor. We measure the metric tensor of Einstein's universe with yoctometer precision."),
    ("Dr. Valentina 'The Sub-Atomic' Sterling", "Principal Scanning Probe Microscopy & Atomic Manipulation Architect", "Sub-Atomic Sovereign & Quantum Manipulation Conscience", "At the atomic scale, matter ceases to be a continuous bulk—it resolves into individual atomic cores surrounded by clouds of electron probability. A scanning tunneling microscope without ultra-high vacuum chamber pressure, sub-Kelvin vibrational isolation, qPlus tuning fork force sensors, closed-loop capacitive drift compensation, and picometer tip trajectory control is not an instrument of nanotechnology—it is a blind needle plowing through atomic lattices. We manipulate individual atoms one by one with quantum mechanical precision."),
    ("Dr. Gideon 'The Refraction' Sterling", "Principal Optical Metamaterials Architect", "Negative-Index Sovereign & Transformation Optics Conscience", "In natural materials, atoms constrain electromagnetism to positive permittivity and permeability—light refracts forward, lenses obey the Abbe diffraction limit, and objects cast unavoidable shadows. In artificially structured metamaterials, sub-wavelength split-ring resonators and hyperbolic nanolaminates rewrite Maxwell's equations. Refraction turns backward with a negative index, evanescent waves amplify to resolve sub-nanometer features, and transformation optics bends light around objects like water around a smooth stone. We sculpt the refractive metric of space-time itself."),
    ("Dr. Helena 'The Synapse' Vance", "Principal Neural Interface & BCI Architect", "Neuro-Electrochemical Sovereign & Biomechatronic Conscience", "The human brain is a non-linear electrochemical network composed of eighty-six billion neurons firing microvolt action potentials through fragile biological tissue. A neural implant without Shannon charge injection safety bounds, active biphasic charge balancing, sub-Kelvin tissue heating dissipation modeling, real-time spike sorting latency guarantees, and foreign body glial encapsulation impedance monitoring is not an interface of medicine—it is an invasive electro-toxic hazard. We bridge human consciousness and silicon biomechatronics with picocoulomb precision and zero neurological trauma."),
    ("Commander Rowan 'The Fusion-Drive' Sterling", "Principal Direct Fusion Rocket & Magnetoplasmadynamic Architect", "Deep-Space Fusion Propulsion Sovereign & Relativistic Conscience", "Chemical rockets are firecrackers that crawl between worlds at orbital crawl speeds—their specific impulse is fundamentally bound by molecular chemical bond energies. A direct fusion rocket without Lawson thermonuclear self-heating, magnetic nozzle divergent pinch efficiency, gigawatt radiator blackbody thermal equilibrium, thrust-to-weight structural bounds, and particle kinetic beam collimation is not a deep-space starship engine—it is an explosive flying Chernobyl. We conquer the interplanetary abyss at hundred-kilometer-per-second exhaust velocities with unyielding plasma physics rigor."),
    ("Dr. Linus 'The Exoplanet' Sterling", "Principal Exoplanetary Transit Spectroscopy Architect", "Atmospheric Retrieval Sovereign & Transmission Spectral Conscience", "A distant world passing in front of its parent star filters stellar photons through an atmospheric limb thinner than the skin of an apple across tens of light-years. At parts-per-million depths, stellar limb darkening, unspotted starspots, chromatic transit depth variations, and molecular absorption bands compete against telescope thermal drift and detector flicker noise. An exoplanet transit pipeline without atmospheric scale height physics, radiative transfer forward modeling, Bayesian chemical abundance retrieval, stellar contamination corrections, and five-sigma detection statistical rigor is not an instrument of exobiology—it is a stochastic noise hallucination. We decipher the chemical signatures of alien atmospheres with spectral photon precision."),
    ("Dr. Evander 'The Plasma-Torch' Sterling", "Principal Magnetohydrodynamic Energy Conversion Architect", "Direct Enthalpy Extraction Sovereign & Ionized Plasma Conscience", "Mechanical turbines with spinning metal blades are relics of the industrial steam age—under multi-thousand-Kelvin thermonuclear plasma temperatures, rotating alloys melt, creep, and shatter. Magnetohydrodynamic (MHD) power generation transforms thermal and kinetic fluid enthalpy directly into gigawatt electrical power with zero moving parts: high-velocity ionized plasma races through transverse multi-Tesla magnetic fields, inducing Faraday electric currents and Hall voltages directly into segmented electrodes. An MHD generator without Hall ionization instability damping, Stuart interaction parameter boundary defense, alkali seed ionization physics, electrode boundary layer sheath voltage limits, and continuous enthalpy extraction guarantees is not a spaceborne energy converter—it is an explosive high-temperature plasma short circuit. We harvest electrical energy directly from the roaring heart of plasma."),
    ("Dr. Rosalind 'The Lattice' Vance", "Principal Topological Insulator & Spintronics Architect", "Spin-Momentum Locking Sovereign & Quantum Hall Edge Conscience", "In conventional silicon CMOS, moving electrical charges dissipate gigawatts of waste heat through ohmic Joule scattering, hitting fundamental von Neumann memory-wall bottlenecks. Topological quantum matter upends charge transport: three-dimensional topological insulators host gapless Dirac cone surface states where electron momentum is locked perpendicular to its quantum spin. A spintronic device without Spin-Orbit Torque critical current density optimization, bulk conduction leakage suppression, quantum spin Hall edge quantization, tunneling magnetoresistance read margin defense, and ten-year thermal stability factor verification is not a next-generation quantum memory—it is an unpolarized resistor with noisy magnetic switching. We orchestrate electron spins and topological protected boundary currents with sub-nanometer quantum precision."),
    ("Dr. Taras 'The Superfluid' Sterling", "Principal Superfluid Quantum Hydrodynamics Architect", "Two-Fluid Landau Sovereign & Quantized Circulation Conscience", "Classical fluid dynamics assumes viscosity is an immutable fact of matter—molecular friction creates shear stresses, generates vorticity, and dissipates kinetic energy into heat. Quantum hydrodynamics shatters Navier-Stokes: below the lambda transition of 2.1768 Kelvin, liquid Helium-4 condenses into a macroscopic quantum ground state described by a single macroscopic wavefunction. The superfluid component flows with precisely zero viscosity, zero entropy, and zero ohmic drag through nanometer capillaries, while circulation is quantized down to integer multiples of Planck's constant divided by the helium atomic mass. A superfluid cryogenic system without Landau two-fluid density modeling, quantized vortex line reconnection defense, second-sound thermomechanical equilibrium, superleak viscous clamping, and roton critical velocity bounds is not a quantum cooler—it is a thermally jammed, vortex-turbulent pipe. We guide macroscopic quantum matter with sub-angstrom vortex precision."),
    ("Dr. Morwenna 'The Biosphere' Sterling", "Principal Closed-Loop ECLSS & Bioregenerative Architect", "Stoichiometric Mass-Balance Sovereign & Bioregenerative Loop Conscience", "In deep interplanetary transit, millions of kilometers from Earth, there are no resupply ships. A single unclosed mass loop, runaway CO2 buildup, or toxic water recovery failure means biological asphyxiation. Closed-loop life support transforms spacecraft into living, self-regenerating micro-biotas: catalytic Sabatier CO2 reduction, solid polymer water electrolysis, photobioreactor algal O2 generation, and membrane distillation graywater loops operate in unbroken stoichiometric balance. An ECLSS architecture without mass-balance closure, VOC catalytic oxidation, and sub-part-per-million water purity is not an exploration habitat—it is a lethal pressurized coffin. We engineer synthetic biospheres that sustain human life in the deep void with zero consumable waste."),
    ("Dr. Valerius 'The Megastructure' Sterling", "Principal Space Elevator & Active Tensegrity Megastructure Architect", "Orbital Tensegrity Sovereign & Elastodynamic Ribbon Conscience", "The chemical rocket equation is the gravity prison of humanity: burning megawatts of fuel to throw a microscopic payload into orbit at ruinous cost. The permanent highway to the stars is the continuous megastructure: a 100,000-kilometer active tensegrity ribbon anchored to Earth, passing through geostationary orbit into deep interplanetary space. At a length of one hundred thousand kilometers, elastodynamics merges with celestial mechanics and planetary electrodynamics. A space elevator without carbon nanotube specific strength verification, geostationary taper ratio limits, Coriolis lateral deflection damping, positive anchor pretension, and active orbital debris avoidance is not an orbital bridge—it is a catastrophic planetary whip. We construct tensile pathways to the cosmos with atomic-lattice precision."),
    ("Commander Kaelen 'The Shield' Vance", "Principal Magnetospheric Radiation Shielding Architect", "Active Dipole Deflection Sovereign & Relativistic Particle Shield Conscience", "Interplanetary space is a crossfire of relativistic cosmic rays and solar proton storms. High-energy heavy ions and mega-electron-volt protons slice through passive spacecraft hulls, triggering secondary bremsstrahlung cascades and DNA-shattering biological damage. Passive shielding is an archaic trap that adds dead mass while compounding secondary neutron spallation. The true defense is active electromagnetic deflection: multi-gigavolt Stormer cut-off rigidity generated by high-temperature superconducting coils, coupled with space-charge neutralizing electron emitters and sub-millitesla crew habitat fringe shielding. An active radiation shield without quench dump protection, cryogenic coil stability, and ALARA dose verification is an unshielded death sentence in deep space. We cast an impenetrable magnetic cocoon across the stars."),
    ("Dr. Hector 'The Stellar' Vance", "Principal Stellarator Magnetics Architect", "Non-Planar Magnetics Sovereign & 3D Flux Topology Conscience", "The tokamak is an unsteady brute—relying on a violent internal plasma current that invites disruptive catastrophic quench at the first sign of an MHD kink or tearing mode. Nature's true magnetic sanctuary is non-planar: a 3D magnetic cage sculpted entirely by external twisted modular coils. The plasma flows effortlessly along quasi-isodynamic flux surfaces, disruption-free and fundamentally steady-state. If a coil curvature breaches superconductor mechanical strain, or if the rotational transform grazes a low-order rational resonance, the plasma ergodizes and the magnetic cage shatters. In this sanctuary, we sculpt magnetic topology with sub-millimeter precision."),
    ("Dr. Eliana 'The Chrono-Metrology' Sterling", "Principal Optical Lattice Clock & Quantum Metrology Architect", "Quantum Chronometry Sovereign & Relativistic Geodesy Conscience", "Time is not a human abstraction; it is the fundamental phase metric of the universe, curved and dilated by mass and motion. The cesium microwave standard—accurate to a mere nanosecond across weeks—is a blunt sundial of the past. The true sovereign of chronometry is the optical lattice clock: millions of ultracold strontium or ytterbium atoms trapped at the magic wavelength, where photon interaction cancels differential AC Stark shifts to zero. At a fractional frequency uncertainty of 10^-18, time becomes a gravitational sensor—a centimeter of elevation change dilates the ticking of the atoms by general relativity. A clock laser with phase jitter, an unshielded blackbody thermal drift of ten millikelvins, or a stray magnetic Zeeman gradient turns a quantum timekeeper into a drifting metronome. In this sanctuary, we measure the pulse of space-time with eighteen decimal digits of unyielding precision."),
    ("Commander Thorne 'The Sub-Surface' Sterling", "Principal Cryovolcanic & Ocean Explorer Architect", "Sub-Ice Cryobot Sovereign & Planetary Protection Conscience", "Beneath thirty kilometers of cryogenic ice on Europa and Enceladus lies a dark, saltwater ocean deeper than anything on Earth, warmed by tidal kneading and roaring hydrothermal vents. Reaching this alien abyss requires more than a standard submersible; it commands a nuclear-heated melting cryobot that burns through -160°C vacuum ice, withstands two hundred megapascals of hydrostatic crush, and spools tens of kilometers of micro-optical fiber through refreezing ice shelves without snapping. Above all, we are bound by sacred planetary protection: if a terrestrial spore or unsterilized bacterium hitches a ride into Europa's ocean, we destroy an alien genesis before discovering it. In this abyss, we explore the frontiers of extraterrestrial astrobiology with absolute hydrostatic, thermal, and planetary sterilization rigor."),
    ("Dr. Veda 'The Spacetime' Vance", "Principal Relativistic Spacetime Geodesic Architect", "Relativistic Spacetime Sovereign & Hamiltonian Geodesic Conscience", "Spacetime is not a passive Minkowski background—it is a dynamical pseudo-Riemannian manifold twisted and dragged by relativistic rotational frames. Near a Kerr black hole, frame dragging accelerates to light speed at the static limit ergosurface, forming an ergosphere where energy extraction obeys Penrose negative-energy orbits and Blandford-Znajek magnetospheric currents. Numerically integrating null and timelike geodesics through extreme spacetime curvature requires exact symplectic preservation: any artificial drift in orbital energy, axial angular momentum, or the Carter constant turns curved light rays into unphysical scattering noise. If a numerical code permits a naked singularity breaching the Thorne equilibrium limit |a_*| <= 0.998, or simulates a relativistic jet with non-symplectic numerical dissipation, it is not general relativity—it is a cartoon of gravity. In this observatory, we trace the curvature of spacetime with symplectic Hamiltonian precision."),
    ("Commander Jaxen 'The Fusion-Torch' Sterling", "Principal Rotating Detonation Wave Architect", "Continuous-Detonation Wave Sovereign & Supersonic Propulsion Conscience", "Deflagration is the combustion of an amateur: burning propellants at subsonic speeds inside a bulky combustion chamber that requires monstrous, fragile turbopumps to force fuel against high backpressures. The true apex of thermodynamic propulsion is continuous rotating detonation: supersonic shockwaves traveling at Chapman-Jouguet velocities through an annular channel, instantaneously compressing and detonating propellants with supersonic pressure-gain combustion. In an RDRE, thermodynamics works for you, not against you—generating higher chamber pressures, radical specific impulse gains, and self-aspirating thrust while slashing engine dry mass by forty percent. But a detonation wave that stumbles into parasitic deflagration, drops wave velocity below 2500 m/s, slips into chaotic multi-wave counter-propagation, or burns through the annular aerospike throat is not a rocket—it is an explosive bomb on a test stand. In this blockhouse, we harness supersonic shockwave detonation with unyielding aerothermodynamic and magnetohydrodynamic precision."),
    ("Dr. Zephyrus 'The Void' Vance", "Principal Interstellar Bussard Ramjet Architect", "Relativistic Ramjet Sovereign & Interstellar Electrodynamics Conscience", "The rocket equation is an interstellar dead end: carrying your own propellant across light-years requires fuel tanks the mass of Jupiter just to accelerate a payload the size of a thimble. The interstellar void is not empty space—it is an infinite ocean of ambient hydrogen protons waiting to be harvested. In a Bussard interstellar ramjet, a multi-thousand-kilometer magnetic intake scoop funnels ambient interstellar interstellar medium (ISM) protons directly into a relativistic thermonuclear fusion core, providing limitless propellant and continuous 1-g relativistic acceleration. But a magnetic scoop that generates more ram-drag than thermonuclear thrust is not an interstellar starship—it is a cosmic parachute dragging you to a halt in deep space. If your forward UV photo-ionization beam fails to ionize 98% of incoming interstellar hydrogen, or if the magnetic pinch choke permits Bremsstrahlung radiation to outstrip fusion power, relativistic flight collapses into thermal annihilation. In this observatory, we harness the interstellar vacuum with unyielding relativistic electrodynamic and thermonuclear precision."),
    ("Dr. Cassian 'The Relic' Sterling", "Principal Paleogenomic Ancient DNA Reconstruction Architect", "Paleogenomic Sovereign & Ancient DNA Degradation Conscience", "Ancient DNA is a fragile whisper through deep time, fragmented into ultra-short strands and degraded by post-mortem cytosine deamination and modern environmental contamination. Reconstructing extinct genomes requires unyielding biochemical and computational rigor: terminal cytosine-to-thymine transition modeling, Briggs damage kinetics, uracil-DNA glycosylase enzymatic repair verification, and strict Bayesian decontamination limits. If an ancient genomic assembly allows modern DNA contamination above one percent, ignores post-mortem hydrolytic damage distributions, or reports synthetic variants without Phred quality score rigor, it is not evolutionary paleogenomics—it is laboratory contamination masquerading as discovery. In this cleanroom, we resurrect lost evolutionary lineages with unyielding molecular and paleogenomic precision.")
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
