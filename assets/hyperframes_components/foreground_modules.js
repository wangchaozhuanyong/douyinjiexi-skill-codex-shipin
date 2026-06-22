(function () {
  function initForegroundModuleRuntime(root) {
    var scope = root || document;
    var modules = Array.prototype.slice.call(scope.querySelectorAll(".hf-module"));
    modules.forEach(function (module, moduleIndex) {
      module.dataset.runtimeReady = "true";
      var micros = Array.prototype.slice.call(module.querySelectorAll(".hf-micro"));
      micros.forEach(function (micro, index) {
        micro.style.animationDelay = 80 + index * 70 + "ms";
        micro.dataset.runtimeReady = "true";
      });
      if (window.gsap) {
        var timeline = window.gsap.timeline({ defaults: { ease: "power3.out" } });
        timeline.fromTo(module, { y: 24, opacity: 0, filter: "blur(8px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.62 }, moduleIndex * 0.03);
        timeline.fromTo(micros, { y: 10, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.42, stagger: 0.07 }, "-=0.24");
        module.dataset.gsapTimeline = "foreground_module_runtime_v1";
      }
    });
    return modules.length;
  }

  window.initForegroundModuleRuntime = initForegroundModuleRuntime;
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initForegroundModuleRuntime(document);
    });
  } else {
    initForegroundModuleRuntime(document);
  }
})();
