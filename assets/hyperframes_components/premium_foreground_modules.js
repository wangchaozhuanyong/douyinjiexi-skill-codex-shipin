(function () {
  "use strict";

  var MODULE_TYPES = [
    "source_evidence_card",
    "three_step_checklist",
    "before_after_compare",
    "test_result_panel",
    "conclusion_stamp",
    "state_lock",
    "node_relay",
    "metric_drum"
  ];

  var LIMITS = {
    title: { maxChars: 18, maxLines: 2 },
    subtitle: { maxChars: 24, maxLines: 1 },
    body: { maxChars: 28, maxLines: 2 },
    chip: { maxChars: 12, maxLines: 1 },
    source: { maxChars: 18, maxLines: 1 }
  };

  var QA_RULES = {
    source_evidence_card: ["requires_unique_source_id", "requires_source_date", "requires_real_screenshot", "requires_conclusion"],
    three_step_checklist: ["requires_three_steps", "requires_equal_grid", "requires_two_line_step_body"],
    before_after_compare: ["requires_two_columns", "requires_change_chip", "requires_matched_baseline"],
    test_result_panel: ["requires_command_or_test", "requires_result", "requires_status"],
    conclusion_stamp: ["requires_final_takeaway", "requires_saveable_template"],
    state_lock: ["requires_state_label", "requires_lock_reason"],
    node_relay: ["requires_two_or_more_nodes", "requires_node_labels"],
    metric_drum: ["requires_metric_values", "requires_takeaway"]
  };

  function text(value) {
    return String(value == null ? "" : value);
  }

  function esc(value) {
    return text(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function cls(value) {
    return text(value).replace(/[^A-Za-z0-9_-]+/g, "-").replace(/^-+|-+$/g, "");
  }

  function clampList(items, limit) {
    return Array.isArray(items) ? items.slice(0, limit) : [];
  }

  function slot(role, label, value, extraClass) {
    return '<div class="pm-slot ' + esc(extraClass || "") + '" data-motion-unit data-role="' + esc(role) + '">' +
      '<span class="pm-slot__label">' + esc(label) + '</span>' +
      '<span class="pm-slot__value">' + esc(value) + '</span>' +
      '</div>';
  }

  function moduleWrap(type, data, inner) {
    var entrance = data.entrance_id || data.entranceId || "micro_component_layer_settle";
    return '<article class="premium-module premium-module--' + esc(cls(type)) + '" data-role="module" data-module-type="' + esc(type) + '" data-entrance-id="' + esc(entrance) + '">' +
      '<header class="pm-header" data-motion-unit>' +
      '<div class="pm-kicker" data-role="kicker">' + esc(data.kicker || data.source_name || data.module_label || "AI / Codex") + '</div>' +
      '<h2 class="pm-title" data-role="headline">' + esc(data.title || data.headline || "主题待绑定") + '</h2>' +
      '</header>' +
      '<section class="pm-body">' + inner + '</section>' +
      '</article>';
  }

  function renderSourceEvidence(data) {
    var screenshot = data.screenshot || data.image || "";
    var media = screenshot
      ? '<img class="pm-proof-image" data-role="proof-image" src="' + esc(screenshot) + '" alt="' + esc(data.source_name || "source proof") + '">'
      : '<div class="pm-proof-image pm-proof-image--missing" data-role="proof-image">SOURCE IMAGE REQUIRED</div>';
    var inner =
      '<div class="pm-evidence-grid">' +
      '<figure class="pm-proof-frame" data-motion-unit data-sfx-cue="proof_tick">' + media + '</figure>' +
      '<div class="pm-proof-meta">' +
      slot("source-chip", "Source", data.source_name || "source", "pm-source-chip") +
      slot("date-pin", "Date", data.source_date || data.date || "date", "pm-date-pin") +
      '<div class="pm-conclusion-bar" data-role="conclusion-bar" data-motion-unit data-sfx-cue="clean_lock_click">' + esc(data.conclusion || "结论待绑定") + '</div>' +
      '</div>' +
      '</div>';
    return moduleWrap("source_evidence_card", data, inner);
  }

  function renderThreeStep(data) {
    var steps = clampList(data.steps || [], 3);
    while (steps.length < 3) steps.push({ label: "Step " + (steps.length + 1), body: "步骤待绑定" });
    var html = steps.map(function (step, index) {
      return '<li class="pm-step" data-motion-unit data-role="step-' + (index + 1) + '" data-sfx-cue="checklist_tick">' +
        '<span class="pm-step__index">' + (index + 1) + '</span>' +
        '<strong>' + esc(step.label || step.title || ("Step " + (index + 1))) + '</strong>' +
        '<span>' + esc(step.body || step.text || "") + '</span>' +
        '</li>';
    }).join("");
    var inner = '<ol class="pm-step-grid">' + html + '</ol>' +
      '<div class="pm-summary-line" data-role="summary-line" data-motion-unit>' + esc(data.summary || "三步讲完，直接照做") + '</div>';
    return moduleWrap("three_step_checklist", data, inner);
  }

  function renderBeforeAfter(data) {
    var inner =
      '<div class="pm-compare-grid">' +
      '<section class="pm-compare-col" data-role="before-column" data-motion-unit>' +
      '<span class="pm-compare-label">' + esc(data.before_label || "Before") + '</span>' +
      '<p>' + esc(data.before || "旧做法待绑定") + '</p>' +
      '</section>' +
      '<section class="pm-compare-col pm-compare-col--after" data-role="after-column" data-motion-unit>' +
      '<span class="pm-compare-label">' + esc(data.after_label || "After") + '</span>' +
      '<p>' + esc(data.after || "新做法待绑定") + '</p>' +
      '</section>' +
      '</div>' +
      '<div class="pm-change-chip" data-role="change-chip" data-motion-unit data-sfx-cue="clean_lock_click">' + esc(data.change || "关键变化") + '</div>';
    return moduleWrap("before_after_compare", data, inner);
  }

  function renderTestResult(data) {
    var rows = clampList(data.rows || [], 3);
    while (rows.length < 3) rows.push({ label: "Check", value: "结果待绑定" });
    var rowHtml = rows.map(function (row, index) {
      var role = index === 0 ? "command-line" : index === 1 ? "output-line" : "result-badge";
      return slot(role, row.label || ("Check " + (index + 1)), row.value || row.text || "", "pm-test-row");
    }).join("");
    var inner = '<div class="pm-test-stack">' + rowHtml + '</div>' +
      '<div class="pm-status-lock" data-role="takeaway-lock" data-motion-unit data-sfx-cue="clean_lock_click">' + esc(data.status || "可执行") + '</div>';
    return moduleWrap("test_result_panel", data, inner);
  }

  function renderConclusion(data) {
    var chips = clampList(data.chips || [], 3);
    while (chips.length < 3) chips.push("结论");
    var chipHtml = chips.map(function (chip, index) {
      var roles = ["source-chip", "step-chip", "result-chip"];
      return '<span class="pm-final-chip" data-role="' + roles[index] + '" data-motion-unit>' + esc(chip) + '</span>';
    }).join("");
    var inner = '<div class="pm-final-chip-row">' + chipHtml + '</div>' +
      '<div class="pm-final-stamp" data-role="final-stamp" data-motion-unit data-sfx-cue="panel_settle">' + esc(data.takeaway || data.conclusion || "保存这条流程") + '</div>';
    return moduleWrap("conclusion_stamp", data, inner);
  }

  function renderStateLock(data) {
    var inner =
      '<div class="pm-state-lock">' +
      '<div class="pm-lock-ring" data-role="lock-ring" data-motion-unit data-sfx-cue="clean_lock_click"></div>' +
      '<div class="pm-state-node" data-role="feedback-node" data-motion-unit>' + esc(data.state || "状态锁定") + '</div>' +
      '<p data-role="support-line" data-motion-unit>' + esc(data.reason || "锁定原因待绑定") + '</p>' +
      '</div>';
    return moduleWrap("state_lock", data, inner);
  }

  function renderNodeRelay(data) {
    var nodes = clampList(data.nodes || [], 5);
    while (nodes.length < 3) nodes.push("节点");
    var html = nodes.map(function (node, index) {
      return '<span class="pm-relay-node" data-role="node-' + (index + 1) + '" data-motion-unit data-sfx-cue="digital_tick">' + esc(node.label || node) + '</span>';
    }).join('<span class="pm-relay-link" data-role="active-connector"></span>');
    var inner = '<div class="pm-relay-path">' + html + '</div>' +
      '<div class="pm-relay-caption" data-role="caption-anchor" data-motion-unit>' + esc(data.caption || "节点按讲解推进") + '</div>';
    return moduleWrap("node_relay", data, inner);
  }

  function renderMetricDrum(data) {
    var metrics = clampList(data.metrics || [], 3);
    while (metrics.length < 3) metrics.push({ label: "Metric", value: "--" });
    var html = metrics.map(function (metric, index) {
      return '<div class="pm-metric" data-role="metric-' + (index + 1) + '" data-motion-unit data-sfx-cue="energy_pulse">' +
        '<strong>' + esc(metric.value || "--") + '</strong>' +
        '<span>' + esc(metric.label || "Metric") + '</span>' +
        '</div>';
    }).join("");
    var inner = '<div class="pm-metric-row">' + html + '</div>' +
      '<div class="pm-metric-takeaway" data-role="takeaway-lock" data-motion-unit data-sfx-cue="clean_lock_click">' + esc(data.takeaway || "结果清楚") + '</div>';
    return moduleWrap("metric_drum", data, inner);
  }

  var RENDERERS = {
    source_evidence_card: renderSourceEvidence,
    three_step_checklist: renderThreeStep,
    before_after_compare: renderBeforeAfter,
    test_result_panel: renderTestResult,
    conclusion_stamp: renderConclusion,
    state_lock: renderStateLock,
    node_relay: renderNodeRelay,
    metric_drum: renderMetricDrum
  };

  function textIssues(value, limit, label) {
    var issues = [];
    var content = text(value).trim();
    if (!content) issues.push(label + " is empty");
    if (content.length > limit.maxChars) issues.push(label + " exceeds " + limit.maxChars + " chars");
    return issues;
  }

  function validateModuleData(type, data) {
    var issues = [];
    if (MODULE_TYPES.indexOf(type) === -1) issues.push("unknown premium module type: " + type);
    issues = issues.concat(textIssues(data.title || data.headline, LIMITS.title, type + ".title"));
    if (type === "source_evidence_card") {
      if (!data.source_id) issues.push(type + ".source_id is required");
      if (!data.source_date && !data.date) issues.push(type + ".source_date is required");
      if (!data.screenshot && !data.image) issues.push(type + ".screenshot is required");
      if (!data.conclusion) issues.push(type + ".conclusion is required");
    }
    if (type === "three_step_checklist" && (!Array.isArray(data.steps) || data.steps.length !== 3)) {
      issues.push(type + ".steps must contain exactly 3 items");
    }
    if (type === "node_relay" && (!Array.isArray(data.nodes) || data.nodes.length < 2)) {
      issues.push(type + ".nodes must contain at least 2 labeled nodes");
    }
    if (type === "metric_drum" && (!Array.isArray(data.metrics) || data.metrics.length < 2)) {
      issues.push(type + ".metrics must contain at least 2 values");
    }
    return issues;
  }

  function validateUniqueEvidenceScreens(modules) {
    var seen = {};
    var issues = [];
    (modules || []).forEach(function (item) {
      if (!item || item.type !== "source_evidence_card") return;
      var image = item.data && (item.data.screenshot || item.data.image);
      if (!image) return;
      if (seen[image]) issues.push("source evidence image reused by " + seen[image] + " and " + (item.data.source_id || "unknown"));
      seen[image] = item.data.source_id || "unknown";
    });
    return issues;
  }

  function render(type, data) {
    if (!RENDERERS[type]) {
      throw new Error("No premium foreground module registered for " + type + ".");
    }
    return RENDERERS[type](data || {});
  }

  function mount(root, modules) {
    var target = typeof root === "string" ? document.querySelector(root) : root;
    if (!target) throw new Error("Premium foreground mount target missing.");
    target.innerHTML = (modules || []).map(function (item) {
      return render(item.type, item.data || {});
    }).join("");
    init(target);
    return target.querySelectorAll(".premium-module").length;
  }

  function init(root) {
    var scope = root || document;
    var modules = Array.prototype.slice.call(scope.querySelectorAll(".premium-module"));
    if (!window.gsap) return modules.length;
    modules.forEach(function (module, moduleIndex) {
      var units = Array.prototype.slice.call(module.querySelectorAll("[data-motion-unit]"));
      var tl = window.gsap.timeline({ defaults: { ease: "power3.out" } });
      tl.fromTo(module, { y: 18, scale: 0.99, autoAlpha: 0, filter: "blur(8px)" }, { y: 0, scale: 1, autoAlpha: 1, filter: "blur(0px)", duration: 0.38 }, moduleIndex * 0.02);
      tl.fromTo(units, { y: 12, autoAlpha: 0, rotateX: -3 }, { y: 0, autoAlpha: 1, rotateX: 0, duration: 0.34, stagger: 0.045 }, "-=0.18");
      module.dataset.premiumRuntimeReady = "true";
    });
    return modules.length;
  }

  window.PremiumForegroundModules = {
    moduleTypes: MODULE_TYPES.slice(),
    limits: JSON.parse(JSON.stringify(LIMITS)),
    qaRules: JSON.parse(JSON.stringify(QA_RULES)),
    render: render,
    mount: mount,
    init: init,
    validateModuleData: validateModuleData,
    validateUniqueEvidenceScreens: validateUniqueEvidenceScreens
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { init(document); });
  } else {
    init(document);
  }
})();
