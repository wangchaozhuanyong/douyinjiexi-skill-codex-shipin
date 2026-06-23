(function () {
  "use strict";

  var TRANSITIONS = [
    "metal_aperture_handoff",
    "glass_prism_refraction",
    "semantic_node_relay",
    "source_evidence_focus",
    "layered_information_assembly",
    "cursor_path_operation",
    "state_lock_microinteraction",
    "checklist_matrix_assembly",
    "proof_lens_magnification",
    "final_template_convergence"
  ];

  var ENTRANCES = [
    "source_proof_snap_in",
    "result_first_plate_reveal",
    "checklist_step_assembly",
    "two_column_compare_build",
    "terminal_proof_rise",
    "cursor_operation_land",
    "metric_lock_sequence",
    "timeline_node_relay_in",
    "final_template_converge_in",
    "micro_component_layer_settle"
  ];

  var TRANSITION_TARGETS = {
    metal_aperture_handoff: [".hf-handoff-chip", ".hf-aperture-frame", ".hf-target-anchor"],
    glass_prism_refraction: [".hf-prism-plate", ".hf-proof-edge", ".hf-target-anchor"],
    semantic_node_relay: [".hf-semantic-node", ".hf-short-path", ".hf-target-slot"],
    source_evidence_focus: [".hf-proof-lens", ".hf-date-pin", ".hf-conclusion-chip"],
    layered_information_assembly: [".hf-layer-title", ".hf-layer-proof", ".hf-layer-action"],
    cursor_path_operation: [".hf-cursor", ".hf-operation-path", ".hf-result-target"],
    state_lock_microinteraction: [".hf-state-node", ".hf-lock-ring", ".hf-target-slot"],
    checklist_matrix_assembly: [".hf-check-item", ".hf-grid-cell", ".hf-check-mark"],
    proof_lens_magnification: [".hf-proof-lens", ".hf-proof-region", ".hf-target-module"],
    final_template_convergence: [".hf-source-chip", ".hf-step-chip", ".hf-result-chip", ".hf-final-template"]
  };

  var ENTRANCE_TARGETS = {
    source_proof_snap_in: ["[data-role='kicker']", "[data-role='headline']", "[data-role='proof-image']", "[data-role='conclusion-bar']"],
    result_first_plate_reveal: ["[data-role='result-value']", "[data-role='headline']", "[data-role='support-line']"],
    checklist_step_assembly: ["[data-role='step-1']", "[data-role='step-2']", "[data-role='step-3']", "[data-role='summary-line']"],
    two_column_compare_build: ["[data-role='before-column']", "[data-role='after-column']", "[data-role='change-chip']"],
    terminal_proof_rise: ["[data-role='command-line']", "[data-role='output-line']", "[data-role='result-badge']"],
    cursor_operation_land: ["[data-role='cursor']", "[data-role='operation-target']", "[data-role='feedback-node']"],
    metric_lock_sequence: ["[data-role='metric-1']", "[data-role='metric-2']", "[data-role='metric-3']", "[data-role='takeaway-lock']"],
    timeline_node_relay_in: ["[data-role='node-1']", "[data-role='node-2']", "[data-role='node-3']", "[data-role='active-connector']"],
    final_template_converge_in: ["[data-role='source-chip']", "[data-role='step-chip']", "[data-role='result-chip']", "[data-role='final-stamp']"],
    micro_component_layer_settle: ["[data-role='primary-component']", "[data-role='secondary-component']", "[data-role='caption-anchor']"]
  };

  function asArray(value) {
    if (!value) return [];
    if (typeof value === "string") return Array.prototype.slice.call(document.querySelectorAll(value));
    if (value.nodeType) return [value];
    return Array.prototype.slice.call(value);
  }

  function scoped(root, selector) {
    if (!root || !selector) return [];
    return Array.prototype.slice.call(root.querySelectorAll(selector));
  }

  function requireGsap() {
    if (!window.gsap) {
      throw new Error("GSAP is required for AdvancedMotionTemplates.");
    }
    return window.gsap;
  }

  function ensureKnown(id, list, kind) {
    if (list.indexOf(id) === -1) {
      throw new Error("No premium " + kind + " template registered for " + id + ".");
    }
  }

  function fromToIf(tl, targets, fromVars, toVars, position) {
    var nodes = asArray(targets);
    if (!nodes.length) return tl;
    return tl.fromTo(nodes, fromVars, toVars, position);
  }

  function toIf(tl, targets, toVars, position) {
    var nodes = asArray(targets);
    if (!nodes.length) return tl;
    return tl.to(nodes, toVars, position);
  }

  function setIf(gsap, targets, vars) {
    var nodes = asArray(targets);
    if (nodes.length) gsap.set(nodes, vars);
  }

  function runEntrance(options) {
    var gsap = requireGsap();
    var root = options.root || document;
    var entranceId = options.entrance_id || options.entranceId;
    var scene = typeof options.scene === "string" ? document.querySelector(options.scene) : options.scene;
    var start = options.start || 0;
    ensureKnown(entranceId, ENTRANCES, "entrance");
    if (!scene) return null;

    var tl = options.timeline || gsap.timeline({ defaults: { ease: "power3.out" } });
    var selectors = ENTRANCE_TARGETS[entranceId] || [];
    var targets = selectors.reduce(function (all, selector) {
      return all.concat(scoped(scene, selector));
    }, []);
    var body = scoped(scene, "[data-role='module'], [data-motion-unit]");

    setIf(gsap, scene, { autoAlpha: 1, pointerEvents: "auto" });
    fromToIf(tl, scene, { autoAlpha: 0.01 }, { autoAlpha: 1, duration: 0.12, ease: "none" }, start);
    fromToIf(tl, body, { y: 18, scale: 0.985, filter: "blur(7px)" }, { y: 0, scale: 1, filter: "blur(0px)", duration: 0.38, stagger: 0.035 }, start + 0.04);
    fromToIf(tl, targets, { y: 16, autoAlpha: 0, rotateX: -5 }, { y: 0, autoAlpha: 1, rotateX: 0, duration: 0.42, stagger: 0.055 }, start + 0.08);
    toIf(tl, scoped(scene, "[data-role='lock-ring'], [data-role='takeaway-lock'], [data-role='final-stamp']"), { scale: 1.025, duration: 0.12, yoyo: true, repeat: 1 }, start + 0.42);
    scene.dataset.motionEntrance = entranceId;
    scene.dataset.contentDeadlineSec = "0.4";
    return tl;
  }

  function runTransition(options) {
    var gsap = requireGsap();
    var recipeId = options.recipe_id || options.recipeId;
    var root = options.root || document;
    var start = options.start || 0;
    ensureKnown(recipeId, TRANSITIONS, "transition");

    var tl = options.timeline || gsap.timeline({ defaults: { ease: "power3.inOut" } });
    var fromScene = typeof options.from_scene === "string" ? document.querySelector(options.from_scene) : options.from_scene;
    var toScene = typeof options.to_scene === "string" ? document.querySelector(options.to_scene) : options.to_scene;
    var veil = scoped(root, ".hf-transition-veil");
    var chip = scoped(root, ".hf-transition-chip");
    var nodes = (TRANSITION_TARGETS[recipeId] || []).reduce(function (all, selector) {
      return all.concat(scoped(root, selector));
    }, []);

    if (toScene) setIf(gsap, toScene, { autoAlpha: 1, pointerEvents: "auto" });
    fromToIf(tl, veil, { scaleX: 0, transformOrigin: "50% 50%", autoAlpha: 0.35 }, { scaleX: 1, autoAlpha: 0.86, duration: 0.18 }, start);
    fromToIf(tl, chip, { y: 10, scale: 0.88, autoAlpha: 0 }, { y: 0, scale: 1, autoAlpha: 1, duration: 0.2 }, start + 0.04);
    fromToIf(tl, nodes, { y: 12, scale: 0.94, autoAlpha: 0 }, { y: 0, scale: 1, autoAlpha: 1, duration: 0.24, stagger: 0.025 }, start + 0.06);
    toIf(tl, fromScene, { autoAlpha: 0, duration: 0.14, ease: "none" }, start + 0.22);
    toIf(tl, veil, { scaleX: 0, autoAlpha: 0, duration: 0.24, transformOrigin: "50% 50%" }, start + 0.26);
    toIf(tl, chip, { y: -8, autoAlpha: 0, duration: 0.16 }, start + 0.26);
    if (toScene) toScene.dataset.motionTransitionIn = recipeId;
    return tl;
  }

  function buildTimeline(motionPlan) {
    var gsap = requireGsap();
    var tl = gsap.timeline();
    (motionPlan.entrances || []).forEach(function (entry) {
      runEntrance(Object.assign({}, entry, { timeline: tl }));
    });
    (motionPlan.transitions || []).forEach(function (entry) {
      runTransition(Object.assign({}, entry, { timeline: tl }));
    });
    return tl;
  }

  function validateRegistry() {
    var issues = [];
    if (TRANSITIONS.length !== 10) issues.push("transition template count must be 10");
    if (ENTRANCES.length !== 10) issues.push("entrance template count must be 10");
    TRANSITIONS.forEach(function (id) {
      if (!TRANSITION_TARGETS[id] || TRANSITION_TARGETS[id].length < 3) issues.push(id + " needs transition target roles");
    });
    ENTRANCES.forEach(function (id) {
      if (!ENTRANCE_TARGETS[id] || ENTRANCE_TARGETS[id].length < 3) issues.push(id + " needs entrance target roles");
    });
    return { ok: issues.length === 0, issues: issues, transitions: TRANSITIONS.slice(), entrances: ENTRANCES.slice() };
  }

  window.AdvancedMotionTemplates = {
    transitions: TRANSITIONS.slice(),
    entrances: ENTRANCES.slice(),
    fromToIf: fromToIf,
    toIf: toIf,
    setIf: setIf,
    runEntrance: runEntrance,
    runTransition: runTransition,
    buildTimeline: buildTimeline,
    validateRegistry: validateRegistry
  };
})();
