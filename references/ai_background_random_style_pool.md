# AI Background Random Style Pool

Use this pool for AI knowledge video generated background plates when the user asks for high-end AI/tech backgrounds. Each video must randomly select one style family before writing `internal/background_prompt_pack.md`, record the selected ID/name, and adapt the selected style into a video-safe background prompt and a unified foreground UI system.

## Random Selection Rule

- Select exactly one `BG_STYLE_01` to `BG_STYLE_15` for the main reusable background plate.
- Record the selected style in `internal/visual_style_decision.json`, `internal/background_prompt_pack.md`, and `asset_manifest.json` as `background_style_pool_id`, `background_style_name`, and `background_style_selection_method`.
- The random selection is once per video, never once per scene. Do not mix quantum blue, black-gold, silver lab, digital city, tunnel, or swarm-network styles in the same video unless the storyboard explicitly documents a two-world comparison.
- The selected style must drive the whole visual system: background palette, light source direction, material family, foreground data panels, caption treatment, transition behavior, and SFX character.
- Do not re-roll the style after script/storyboard lock unless QA fails for readability, background text, clutter, or topic mismatch.
- If multiple generated background variants are needed in one video, keep them within the selected style family unless the storyboard explicitly needs a transition into a second world.
- The raw style descriptions are style seeds, not direct copy-paste prompts. Rewrite them with the visual-director fields required by `references/ai_generated_asset_prompt_system.md`.
- Read `references/enterprise_ai_control_console_visual_system.md` after selecting the style and before designing foreground components.

## Video-Safe Adaptation

The user's source styles use dense, full-frame futuristic structures. For video backgrounds, translate `full-frame` and `no blank area` as:

```text
rich full-frame atmosphere with no cheap empty wallpaper, but with controlled low-detail text-safe zones created by depth of field, vignette, lower contrast, haze, and clean lighting falloff.
```

Never interpret `no blank area` as permission to place bright lines, particles, chips, nodes, grids, or hard edges under Chinese captions, titles, proof cards, or CTA text. If the selected style is visually dense, reduce local contrast behind foreground content, blur or darken the safe band, and keep the most complex structures away from reading zones.

All styles keep these global constraints:

- 16:9 horizontal AI knowledge video background unless a routed exception exists.
- No readable Chinese, English, letters, numbers, formulas, code, logos, watermarks, UI labels, fake dashboards, or brand marks.
- No people, faces, hands, robot characters, or mascot-like robots.
- No fake official UI, fake proof, fake analytics, or screenshot-like evidence.
- No unused layout skeleton, placeholder cards, empty UI slots, or workflow wireframes.
- Must reserve title/caption/proof safe zones through lighting and low-detail atmosphere.

## Style Pool

### BG_STYLE_01: 量子环形反应堆

Core visual: a giant 3D quantum ring reactor with transparent concentric rings, a glowing polyhedral intelligent core, neural-network nodes, quantum particles, crystal computing modules, and precise data routes converging into the center.

Best for: model reasoning, super-compute, quantum AI, AI infrastructure, high-end launch visuals.

Palette/material: deep navy, black-blue, electric cyan, ice blue, violet, teal-green; transparent crystal, smoked glass, precision metal, fiber optics, holographic energy, liquid light.

Video-safe prompt direction: keep the reactor as the dominant center or right-side focal subject, push the densest cables and particle structures toward the edges, and create a calm lower-third or side caption zone with haze and controlled falloff.

### BG_STYLE_02: 芯片峡谷超级计算机

Core visual: a single-point-perspective supercomputer canyon with towering server walls, GPU units, transparent chip layers, cooling structures, fiber interfaces, and a glowing data channel receding into depth.

Best for: compute power, AI infrastructure, coding tools, automation backends, reliability and speed.

Palette/material: black-blue, deep cyan-blue, electric cyan, ice blue, teal-green, slight violet-blue; precision metal, semiconductor surfaces, frosted glass, transparent crystal, fiber optics, liquid energy.

Video-safe prompt direction: preserve the strong vanishing point and canyon scale, but keep the central data path smooth enough for foreground cards or captions; avoid tiny chip text and brand-like details.

### BG_STYLE_03: 全息数字孪生都市

Core visual: a holographic digital twin city made of transparent data towers, crystal skyscrapers, server buildings, chip architecture, computing centers, energy pillars, floating platforms, and AI control hubs.

Best for: digital twin, enterprise AI, smart city, cloud AI, industrial AI, ecosystem or platform topics.

Palette/material: deep blue, black-blue, electric cyan, purple-red, teal-green, ice blue; transparent glass, holographic linework as texture, precision metal, luminous circuits.

Video-safe prompt direction: use the city as an atmospheric world, not a literal skyline with signs. Keep building detail away from title/caption bands and remove all billboard-like surfaces.

### BG_STYLE_04: 生物神经森林

Core visual: a bio-neural forest where neural networks, dendritic branches, synapses, bio-fiber optics, data mycelium, transparent membranes, and DNA-like double helices form a digital life system.

Best for: neural networks, bio-inspired AI, medical AI, brain science, self-learning systems, adaptive agents.

Palette/material: deep cyan-black, emerald green, electric cyan, ice blue, purple-red, subtle warm gold; transparent bio-membrane, crystal, liquid light, fiber optics, glass, organic metal.

Video-safe prompt direction: make it mysterious and elegant rather than biological horror. Avoid real organs, blood, medical textbook visuals, and keep foreground text over darker haze or softly blurred neural branches.

### BG_STYLE_05: 晶体张量矩阵

Core visual: a crystalline tensor matrix with transparent crystals, polyhedra, floating cubes, triangular mesh, tensor modules, glass chips, optical lattices, and luminous nodes.

Best for: AI algorithms, tensor computation, machine learning, mathematical models, research computing, AI lab visuals.

Palette/material: deep blue, ice blue, electric cyan, violet, teal-green, silver-white highlights; high-purity crystal, optical glass, precision metal, holographic film, liquid energy.

Video-safe prompt direction: keep the geometry clean, precise, and non-repetitive. Use depth of field and controlled refraction so crystal edges do not cut through captions.

### BG_STYLE_06: 黑金机械量子引擎

Core visual: a luxurious black-gold mechanical quantum engine with black metal rings, champagne-gold frames, smoked glass, precision gears, quantum chips, crystal bearings, and a glowing intelligent core.

Best for: finance AI, enterprise strategy, high-end platforms, executive technology, powerful agent systems, premium launch visuals.

Palette/material: deep black, black-blue, gunmetal, champagne gold, small electric cyan, ice blue, violet; brushed metal, smoked glass, mirror metal, transparent crystal, fiber optics, liquid energy.

Video-safe prompt direction: keep black-gold contrast restrained and elegant. Avoid steampunk, clock markings, cheap gold, or dense gear edges behind subtitles.

### BG_STYLE_07: 银白光子实验室

Core visual: a bright silver-white photon AI laboratory with a transparent photon computing core, silver frames, ice-blue crystal, optical chips, photon tracks, neural nodes, and clean research equipment.

Best for: scientific AI, education AI, medical AI, photon chips, research labs, trustworthy enterprise R&D.

Palette/material: white, silver gray, ice blue, light cyan, transparent glass, slight pale violet; frosted glass, high-purity crystal, silver metal, optical acrylic, holographic film, fiber optics.

Video-safe prompt direction: preserve cleanliness and trust, but prevent overexposure. Use soft gray or ice-blue safe zones for Chinese captions and proof cards.

### BG_STYLE_08: 等离子数据风暴

Core visual: a high-speed plasma data vortex made of millions of particles, glowing fibers, energy bands, spatial curves, algorithm pulses, data nodes, and a transparent fluid-like AI core.

Best for: big data, real-time inference, generative AI, model training, search/recommendation, high-concurrency computing.

Palette/material: black-blue, deep purple, electric cyan, purple-red, ice blue, small teal and white highlights; plasma, fiber optics, transparent crystal, holographic energy, micro-particles.

Video-safe prompt direction: keep motion energy as directional flow, not chaotic noise. Lower particle density behind captions and avoid fireworks, flame, or uncontrolled storm visuals.

### BG_STYLE_09: 翡翠量子隧道

Core visual: an emerald quantum tunnel with layered hexagonal frames, crystal rings, energy tracks, neural nodes, fiber channels, precision circuitry, and a distant AI quantum core.

Best for: AI data transmission, model inference channels, quantum communication, cybersecurity, network routing, future computing.

Palette/material: deep black, ink green, emerald green, electric cyan, ice blue, small violet energy; emerald crystal, smoked glass, precision metal, transparent fiber optics, holographic energy.

Video-safe prompt direction: preserve the strong tunnel perspective and speed, but keep the vanishing path from becoming a hard line through subtitles. Avoid subway, spaceship, vehicle, or cheap green neon associations.

### BG_STYLE_10: 群体智能轨道网络

Core visual: a distributed swarm-intelligence orbital network with transparent intelligent spheres, independent neural cores, polyhedral processors, data nodes, orbital systems, and multi-agent connection paths.

Best for: multi-agent systems, Agent collaboration, distributed AI, cloud-edge coordination, AI ecosystem platforms, task orchestration.

Palette/material: deep blue, black-blue, electric cyan, violet, teal-green, ice-blue highlights; transparent glass, crystal, metal, fiber optics, holographic energy, liquid light.

Video-safe prompt direction: keep the system complex and ordered, not like a simple solar system. Use foreground blur and clean atmospheric gaps so titles and captions remain readable.

### BG_STYLE_11: AI宇宙意识网络

Core visual: a planet-scale artificial-intelligence consciousness core suspended in deep space, built from transparent crystal compute cabins, titanium mechanical structure, multilayer quantum processors, neural nodes, optical-fiber matrices, orbital rings, satellites, space platforms, and interplanetary connection paths. The world should feel like an intelligent cosmic network rather than a simple glowing sphere.

Best for: frontier AI, model intelligence, AGI debate, multi-agent civilization, distributed reasoning, AI infrastructure at cosmic scale, epic opening/cover visuals.

Palette/material: deep-space black, dark blue, ice blue, silver white, cold cyan, restrained violet, small amber star light; titanium alloy, aerospace ceramic, transparent crystal, smoked glass, carbon fiber, optical fiber, high-density plasma, physically plausible star haze.

Video-safe prompt direction: keep the main consciousness core as a center/right deep focal subject and use foreground/midground/background depth to create scale. Dense orbital structures, nodes, and light-fiber paths must not cross title, caption, or proof zones. Use cosmic haze, depth of field, and low-contrast safe bands so the epic background remains readable in a video frame.

### BG_STYLE_12: AI机械文明巨构

Core visual: a city-scale AI mechanical civilization megastructure: giant metal pillars, mechanical ribs, ring compute structures, vertical server towers, energy pipes, liquid-cooling systems, bridges, structural frames, and a suspended central consciousness processor inside a monumental industrial temple.

Best for: AI infrastructure, automation factories, coding backends, enterprise AI foundations, model deployment, reliable system architecture, powerful tool-chain videos.

Palette/material: gunmetal, black, steel blue, titanium, concrete gray, restrained ice-blue device light, amber energy light; real steel, titanium alloy, heat-resistant ceramic, industrial glass, copper, concrete, composite armor, oil marks, worn edges, heat haze.

Video-safe prompt direction: preserve low-angle architectural scale and real engineering logic, but avoid turning the frame into a cluttered factory. Keep the densest pipes, beams, cables, and towers away from Chinese text lanes. Use industrial fog, air perspective, and dark matte foreground surfaces for readable overlays.

### BG_STYLE_13: 星球环形AI计算都市

Core visual: an artificial-intelligence ring city around a massive planet, made of compute buildings, data centers, server towers, quantum processing stations, energy platforms, orbital ports, communication facilities, solar arrays, mechanical bridges, distributed AI cores, and realistic aerospace infrastructure.

Best for: cloud AI, distributed computing, global AI networks, smart cities, enterprise platforms, AI ecosystems, planet-scale infrastructure explanations.

Palette/material: deep-space black, silver gray, ice blue, cold white, electric cyan, restrained warm city lights, small golden stellar light; aerospace metal, titanium alloy, ceramic insulation, transparent crystal, glass, solar material, optical fiber.

Video-safe prompt direction: use the planet curve and ring city as the visual thesis, not as a sign-filled skyline. Keep city lights and bridge lines from forming distracting grids behind captions. Reserve calm atmospheric regions through planet shadow, cloud haze, and smooth orbital depth for foreground proof panels.

### BG_STYLE_14: 黑金AI恒星引擎

Core visual: a luxurious black-gold artificial-intelligence stellar engine in deep space, with smoked glass, obsidian metal, brushed titanium, champagne-gold frames, transparent crystal processors, quantum compute modules, energy pipes, magnetic stabilization rings, and a controlled miniature star or fusion core.

Best for: premium AI platforms, executive strategy, finance AI, high-end agents, powerful workflow systems, luxury launch covers, authority and trust visuals.

Palette/material: deep black, gunmetal, black-blue, smoked glass, champagne gold under 20%, small ice-blue/cold-white/emerald device lights; brushed metal, mirror titanium, obsidian, crystal, ceramic, carbon fiber, restrained warm core glow.

Video-safe prompt direction: keep the black-gold language elegant and controlled. The gold should come from the core light and structural edges, not cheap jewelry color. Use the stellar engine as a dominant focal object while keeping a dark low-detail overlay zone for titles, captions, and proof cards.

### BG_STYLE_15: AI机械天空之城

Core visual: a bright artificial-intelligence mechanical sky city above a cloud sea, built from multilayer city platforms, AI control towers, server skyscrapers, transparent crystal buildings, ring transit systems, mechanical bridges, energy platforms, anti-gravity bases, space elevators, orbit-linked towers, and distant suspended cities.

Best for: education AI, creative tools, clean enterprise AI, smart city, cloud-to-space infrastructure, hopeful future AI, beginner-friendly but premium explainers.

Palette/material: silver gray, steel blue, deep black, ice blue, cold white, warm city light, amber sunlight; steel, titanium alloy, glass, concrete, carbon fiber, transparent crystal, volumetric clouds, atmospheric scattering.

Video-safe prompt direction: preserve the bright epic city and cloud depth while avoiding overexposed white surfaces. Put the most complex building clusters away from captions and use soft cloud haze, sky gradients, and muted metal platforms as readable foreground stages. No flying-car hero shots, anime sky city, or billboard-like surfaces.
