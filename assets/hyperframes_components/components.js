(function () {
  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function proofFrame(asset, label) {
    var src = asset || "";
    var labelHtml = label ? '<div class="hf-callout-chip">' + escapeHtml(label) + "</div>" : "";
    return [
      '<div class="hf-proof-frame" data-motion="source_focus_lens_reveal">',
      src ? '<img src="' + escapeHtml(src) + '" alt="' + escapeHtml(label || "proof asset") + '">' : "",
      labelHtml,
      "</div>",
    ].join("");
  }

  function caption(text) {
    if (!text) return "";
    return '<div class="hf-caption-rail"><div class="hf-caption-text">' + escapeHtml(text) + "</div></div>";
  }

  function stage(content, captionText) {
    return '<section class="hf-ai-stage"><div class="hf-safe-frame">' + content + "</div>" + caption(captionText) + "</section>";
  }

  function ColdOpenProofCard(opts) {
    opts = opts || {};
    return stage(
      [
        '<div class="hf-cold-open-proof">',
        "<div>",
        '<div class="hf-eyebrow">' + escapeHtml(opts.eyebrow || "HOOK CONFLICT") + "</div>",
        '<h1 class="hf-title">' + escapeHtml(opts.headline || "错误问法") + "</h1>",
        '<p class="hf-muted" style="font-size:34px;line-height:1.35;margin-top:28px;">' + escapeHtml(opts.subline || "先让观众看见问题，不先讲概念。") + "</p>",
        "</div>",
        proofFrame(opts.proof_asset, opts.proof_label || "真实操作证据"),
        "</div>",
      ].join(""),
      opts.caption
    );
  }

  function SourceWallGrid(opts) {
    opts = opts || {};
    var assets = opts.proof_assets || [];
    var labels = opts.labels || [];
    var cards = assets.slice(0, 3).map(function (asset, index) {
      return '<div class="hf-source-card hf-panel">' + proofFrame(asset, labels[index] || "source") + "</div>";
    });
    return stage(
      [
        '<div class="hf-eyebrow">SOURCE PROOF</div>',
        '<h1 class="hf-title" style="font-size:72px;margin-bottom:34px;">' + escapeHtml(opts.headline || "来源证据") + "</h1>",
        '<div class="hf-source-wall-grid" data-motion="citation_rail_wipe">',
        cards.join(""),
        "</div>",
      ].join(""),
      opts.caption
    );
  }

  function OperationSimulation(opts) {
    opts = opts || {};
    var steps = opts.steps || ["目标", "约束", "检查点"];
    return stage(
      [
        '<div class="hf-operation-simulation" data-motion="operation_node_relay">',
        '<div class="hf-brief hf-panel"><div class="hf-eyebrow">TASK BRIEF</div><h2>' + escapeHtml(opts.brief || "任务说明") + "</h2></div>",
        '<div class="hf-workspace hf-panel"><div class="hf-eyebrow">WORKSPACE</div><h1 style="font-size:58px;line-height:1.08;">' + escapeHtml(opts.workspace || "真实执行过程") + "</h1></div>",
        '<div class="hf-result-rail hf-panel">' + steps.map(function (step, index) {
          return '<div class="hf-callout-chip" style="margin:0 0 16px 0;">' + String(index + 1).padStart(2, "0") + " " + escapeHtml(step) + "</div>";
        }).join("") + "</div>",
        "</div>",
      ].join(""),
      opts.caption
    );
  }

  function ProcessRail(opts) {
    opts = opts || {};
    var steps = opts.steps || ["目标", "环境", "检查点", "验收"];
    return stage(
      [
        '<div class="hf-eyebrow">METHOD RAIL</div>',
        '<h1 class="hf-title" style="font-size:72px;margin-bottom:34px;">' + escapeHtml(opts.headline || "把方法拆成流程") + "</h1>",
        '<div class="hf-process-rail" data-motion="template_lift_settle">',
        steps.map(function (step, index) {
          return '<div class="hf-process-step hf-panel"><div class="hf-step-index">' + String(index + 1) + '</div><h2 style="font-size:42px;">' + escapeHtml(step) + "</h2></div>";
        }).join(""),
        "</div>",
      ].join(""),
      opts.caption
    );
  }

  function EvidenceResultCard(opts) {
    opts = opts || {};
    var lines = opts.lines || ["check: passed", "risk: closed", "evidence: ready"];
    return stage(
      [
        '<div class="hf-evidence-result-card" data-motion="terminal_scan_proof_tray">',
        '<div class="hf-terminal">' + lines.map(function (line) {
          return '<div>&gt; ' + escapeHtml(line) + "</div>";
        }).join("") + "</div>",
        '<div class="hf-panel" style="padding:38px;"><div class="hf-eyebrow">RESULT</div><h1 style="font-size:62px;line-height:1.05;">' + escapeHtml(opts.result || "证据包生成") + "</h1></div>",
        "</div>",
      ].join(""),
      opts.caption
    );
  }

  function FinalTemplate(opts) {
    opts = opts || {};
    return stage(
      [
        '<div class="hf-final-template hf-panel" data-motion="final_controlled_zoom">',
        '<div class="hf-eyebrow">SAVE TEMPLATE</div>',
        '<div class="hf-formula">' + escapeHtml(opts.formula || "目标 + 环境 + 检查点 + 验收") + "</div>",
        '<div class="hf-save-chip">' + escapeHtml(opts.cta || "收藏这条，直接套用") + "</div>",
        "</div>",
      ].join(""),
      opts.caption
    );
  }

  window.HyperFramesAIComponents = {
    ColdOpenProofCard: ColdOpenProofCard,
    SourceWallGrid: SourceWallGrid,
    ProofWallGrid: SourceWallGrid,
    OperationSimulation: OperationSimulation,
    EvidenceResultCard: EvidenceResultCard,
    ProcessRail: ProcessRail,
    FinalTemplate: FinalTemplate,
  };
})();
