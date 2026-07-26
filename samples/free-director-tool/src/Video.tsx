import type {Caption} from "@remotion/captions";
import {Audio} from "@remotion/media";
import React, {useCallback, useEffect, useState} from "react";
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useDelayRender,
  useVideoConfig,
} from "remotion";
import blockedJson from "../proof/blocked-validation.json";
import passedJson from "../proof/passed-validation.json";
import storyboard from "../storyboard.json";

const blocked = blockedJson as {
  status: string;
  blocking_issues: string[];
};
const passed = passedJson as {
  status: string;
  summary: {
    claims: number;
    beats: number;
    scenes: number;
    assets: number;
    canonical_renderer: string;
  };
};

const COLORS = {
  ink: "#0B1020",
  paper: "#F5F1E8",
  red: "#FF4D4D",
  green: "#A6FF4D",
  blue: "#2457FF",
  lilac: "#C5B8FF",
  pink: "#FF8CC6",
  white: "#FFFFFF",
};

const FONT =
  '"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif';
const MONO = '"SFMono-Regular", "Menlo", "Monaco", monospace';

const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

const easeOut = (frame: number, from = 0, duration = 20) =>
  interpolate(frame, [from, from + duration], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

const safe: React.CSSProperties = {
  position: "absolute",
  top: 92,
  left: 62,
  right: 142,
  bottom: 258,
};

const Kicker: React.FC<{
  left: string;
  right: string;
  color?: string;
}> = ({left, right, color = COLORS.green}) => (
  <div
    style={{
      position: "absolute",
      top: 48,
      left: 62,
      right: 142,
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      color,
      fontFamily: MONO,
      fontWeight: 800,
      fontSize: 22,
      letterSpacing: 1.5,
      zIndex: 30,
    }}
  >
    <span>{left}</span>
    <span>{right}</span>
  </div>
);

const Grid: React.FC<{color?: string; opacity?: number}> = ({
  color = COLORS.white,
  opacity = 0.08,
}) => (
  <AbsoluteFill
    style={{
      opacity,
      backgroundImage: `linear-gradient(${color} 1px, transparent 1px), linear-gradient(90deg, ${color} 1px, transparent 1px)`,
      backgroundSize: "54px 54px",
    }}
  />
);

const Cursor: React.FC<{progress: number; top?: number}> = ({
  progress,
  top = 162,
}) => (
  <div
    style={{
      position: "absolute",
      top,
      left: 62,
      width: interpolate(progress, [0, 1], [42, 870]),
      height: 8,
      background: COLORS.green,
      boxShadow: `0 0 30px ${COLORS.green}`,
      zIndex: 25,
    }}
  />
);

const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const cut = frame === 0 ? 1 : easeOut(frame, 10, 24);
  const report = frame === 0 ? 1 : easeOut(frame, 24, 20);
  const issue =
    blocked.blocking_issues.find((item) => item.includes("proof")) ??
    blocked.blocking_issues[0] ??
    "storyboard proof id is missing from asset manifest";
  return (
    <AbsoluteFill style={{background: COLORS.ink, fontFamily: FONT, color: COLORS.white}}>
      <Grid />
      <Kicker left="AI VIDEO / DIAGNOSIS" right="CLAIM 01 · BLOCKED" />
      <Cursor progress={easeOut(frame, 0, 30)} />
      <div style={safe}>
        <div
          style={{
            position: "absolute",
            top: 120,
            left: 0,
            fontSize: 112,
            lineHeight: 0.92,
            fontWeight: 950,
            letterSpacing: -7,
          }}
        >
          有字幕
          <br />
          有动效
          <br />
          <span style={{color: COLORS.red}}>为什么还不行？</span>
        </div>
        <div
          style={{
            position: "absolute",
            top: 650,
            left: interpolate(cut, [0, 1], [700, 0]),
            right: 0,
            height: 500,
            background: COLORS.paper,
            color: COLORS.ink,
            borderRadius: 32,
            padding: 36,
            transform: `rotate(${interpolate(cut, [0, 1], [6, -1.4])}deg)`,
            boxShadow: "0 35px 100px rgba(0,0,0,.42)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontFamily: MONO,
              fontWeight: 900,
              fontSize: 24,
            }}
          >
            <span>validation_report.json</span>
            <span
              style={{
                background: COLORS.red,
                color: COLORS.white,
                borderRadius: 99,
                padding: "10px 18px",
              }}
            >
              {blocked.status.toUpperCase()}
            </span>
          </div>
          <div
            style={{
              marginTop: 44,
              fontSize: 50,
              lineHeight: 1.12,
              fontWeight: 900,
              opacity: interpolate(report, [0, 1], [0.25, 1]),
            }}
          >
            旁白说了结果
            <br />
            <span style={{color: COLORS.red}}>画面没有 proof</span>
          </div>
          <div
            style={{
              marginTop: 36,
              paddingTop: 24,
              borderTop: `3px solid ${COLORS.ink}`,
              fontFamily: MONO,
              fontSize: 22,
              lineHeight: 1.45,
            }}
          >
            {issue.replace(/\/private\/[^ ]+/g, "[sanitized-path]")}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const InputScene: React.FC = () => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, 0, 22);
  const items = [
    ["TASK", "讲清 claim-proof 为什么会阻止空口结论"],
    ["INPUT", "真实 source / script / storyboard / asset"],
    ["PROCESS", "先失败一次，再修复并重跑"],
    ["RESULT", "显示 BLOCKED → PASSED 的真实报告"],
  ];
  return (
    <AbsoluteFill style={{background: COLORS.paper, color: COLORS.ink, fontFamily: FONT}}>
      <Kicker left="REAL INPUT / NOT A TEMPLATE" right="PROOF P2" color={COLORS.blue} />
      <Cursor progress={easeOut(frame, 0, 32)} />
      <div style={safe}>
        <div
          style={{
            position: "absolute",
            top: 126,
            left: 0,
            right: 0,
            fontWeight: 950,
            fontSize: 88,
            lineHeight: 0.98,
            letterSpacing: -5,
          }}
        >
          第一步
          <br />
          <span style={{color: COLORS.blue}}>不是选模板</span>
        </div>
        <div
          style={{
            position: "absolute",
            top: 430,
            left: interpolate(enter, [0, 1], [110, 0]),
            right: 0,
            background: COLORS.white,
            border: `4px solid ${COLORS.ink}`,
            borderRadius: 30,
            overflow: "hidden",
            boxShadow: `20px 24px 0 ${COLORS.lilac}`,
          }}
        >
          <div
            style={{
              height: 64,
              background: COLORS.ink,
              color: COLORS.green,
              padding: "17px 26px",
              fontFamily: MONO,
              fontSize: 22,
              fontWeight: 800,
            }}
          >
            user-input.txt
          </div>
          <div style={{padding: "20px 28px 30px"}}>
            {items.map(([label, value], index) => {
              const itemEnter = easeOut(frame, 12 + index * 12, 18);
              return (
                <div
                  key={label}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "150px 1fr",
                    gap: 20,
                    padding: "24px 0",
                    borderBottom:
                      index === items.length - 1
                        ? "none"
                        : `2px solid ${COLORS.ink}`,
                    opacity: itemEnter,
                    transform: `translateX(${interpolate(itemEnter, [0, 1], [70, 0])}px)`,
                  }}
                >
                  <strong
                    style={{
                      fontFamily: MONO,
                      fontSize: 23,
                      color: index === 3 ? COLORS.red : COLORS.blue,
                    }}
                  >
                    {label}
                  </strong>
                  <span style={{fontSize: 31, fontWeight: 780, lineHeight: 1.3}}>
                    {value}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            bottom: 40,
            right: 0,
            color: COLORS.blue,
            fontFamily: MONO,
            fontWeight: 900,
            fontSize: 22,
          }}
        >
          INPUT DEFINES THE EVIDENCE
        </div>
      </div>
    </AbsoluteFill>
  );
};

const PipelineScene: React.FC = () => {
  const frame = useCurrentFrame();
  const nodes = [
    ["SOURCE", "validate_project.py"],
    ["BEAT", "B1 / narration claim"],
    ["SCENE", "SC1 / diagnostic split"],
    ["PROOF", "P1 / blocked-validation.json"],
  ];
  return (
    <AbsoluteFill style={{background: "#121A16", color: COLORS.white, fontFamily: FONT}}>
      <Grid color={COLORS.green} opacity={0.1} />
      <Kicker left="CLAIM → PROOF / SAME MOMENT" right="EXECUTION" />
      <Cursor progress={easeOut(frame, 0, 30)} />
      <div style={safe}>
        <div
          style={{
            position: "absolute",
            top: 116,
            fontSize: 76,
            lineHeight: 1,
            fontWeight: 950,
            letterSpacing: -4,
          }}
        >
          每句话
          <br />
          都要接上<span style={{color: COLORS.green}}>真实证据</span>
        </div>
        <div
          style={{
            position: "absolute",
            top: 408,
            left: 18,
            width: 8,
            height: 890,
            background: "rgba(166,255,77,.18)",
          }}
        >
          <div
            style={{
              width: "100%",
              height: interpolate(easeOut(frame, 16, 90), [0, 1], [0, 890]),
              background: COLORS.green,
              boxShadow: `0 0 30px ${COLORS.green}`,
            }}
          />
        </div>
        <div style={{position: "absolute", top: 372, left: 68, right: 0}}>
          {nodes.map(([label, value], index) => {
            const itemEnter = easeOut(frame, 15 + index * 24, 18);
            return (
              <div
                key={label}
                style={{
                  position: "relative",
                  minHeight: 205,
                  padding: "26px 28px",
                  marginBottom: 18,
                  border: `2px solid rgba(255,255,255,.3)`,
                  background:
                    index === 3 ? "rgba(166,255,77,.13)" : "rgba(255,255,255,.055)",
                  opacity: itemEnter,
                  transform: `translateX(${interpolate(itemEnter, [0, 1], [120, 0])}px)`,
                }}
              >
                <div
                  style={{
                    fontFamily: MONO,
                    fontSize: 21,
                    fontWeight: 900,
                    color: COLORS.green,
                  }}
                >
                  0{index + 1} / {label}
                </div>
                <div
                  style={{
                    marginTop: 18,
                    fontFamily: MONO,
                    fontSize: 30,
                    fontWeight: 800,
                    lineHeight: 1.25,
                  }}
                >
                  {value}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const DirectorScene: React.FC = () => {
  const frame = useCurrentFrame();
  const concepts = [
    {name: "证据轨道", sub: "流程清楚 / 容易变信息图", color: COLORS.lilac},
    {name: "屏幕手术台", sub: "切开问题 / 直接看修复", color: COLORS.green},
    {name: "杂志剖面", sub: "视觉丰富 / 报告容易变小", color: COLORS.pink},
  ];
  return (
    <AbsoluteFill
      style={{
        background: COLORS.blue,
        color: COLORS.white,
        fontFamily: FONT,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          width: 900,
          height: 900,
          borderRadius: "50%",
          background: COLORS.pink,
          top: -390,
          right: -420,
          transform: `scale(${interpolate(easeOut(frame, 0, 45), [0, 1], [0.7, 1])})`,
        }}
      />
      <Kicker left="FREE DIRECTOR / 3 REAL CONCEPTS" right="PROOF P4" />
      <Cursor progress={easeOut(frame, 0, 32)} />
      <div style={safe}>
        <div
          style={{
            position: "absolute",
            top: 110,
            left: 0,
            fontSize: 84,
            fontWeight: 950,
            lineHeight: 0.95,
            letterSpacing: -5,
          }}
        >
          每条视频
          <br />
          <span style={{color: COLORS.green}}>重新决定视觉语言</span>
        </div>
        <div style={{position: "absolute", top: 432, left: 0, right: 0}}>
          {concepts.map((concept, index) => {
            const itemEnter = easeOut(frame, 12 + index * 16, 18);
            const selected = index === 1 && frame > 72;
            return (
              <div
                key={concept.name}
                style={{
                  height: selected ? 285 : 235,
                  marginBottom: 24,
                  padding: "32px 34px",
                  border: `4px solid ${COLORS.white}`,
                  background: selected ? concept.color : "rgba(11,16,32,.26)",
                  color: selected ? COLORS.ink : COLORS.white,
                  transform: `translateX(${interpolate(itemEnter, [0, 1], [index % 2 ? 120 : -120, 0])}px) rotate(${selected ? -1.2 : 0}deg)`,
                  opacity: itemEnter,
                  boxShadow: selected ? `18px 20px 0 ${COLORS.ink}` : "none",
                }}
              >
                <div
                  style={{
                    fontFamily: MONO,
                    fontWeight: 900,
                    fontSize: 22,
                    opacity: 0.8,
                  }}
                >
                  CONCEPT 0{index + 1} {selected ? "/ SELECTED" : ""}
                </div>
                <div style={{fontSize: 58, fontWeight: 950, marginTop: 8}}>
                  {concept.name}
                </div>
                <div style={{fontSize: 26, fontWeight: 700, marginTop: 8}}>
                  {concept.sub}
                </div>
              </div>
            );
          })}
        </div>
        <div
          style={{
            position: "absolute",
            bottom: 24,
            left: 0,
            right: 0,
            display: "flex",
            gap: 16,
            flexWrap: "wrap",
            fontFamily: MONO,
            fontSize: 19,
            fontWeight: 900,
          }}
        >
          {["黑板皮肤", "银河背景", "重复卡片", "计时器强制切镜"].map((item) => (
            <span
              key={item}
              style={{
                color: COLORS.white,
                border: `2px solid ${COLORS.white}`,
                padding: "9px 12px",
                textDecoration: "line-through",
                background: COLORS.red,
              }}
            >
              {item}
            </span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const PassScene: React.FC = () => {
  const frame = useCurrentFrame();
  const status = easeOut(frame, 22, 22);
  const timeline = easeOut(frame, 64, 44);
  return (
    <AbsoluteFill style={{background: COLORS.paper, color: COLORS.ink, fontFamily: FONT}}>
      <Kicker left="REAL EXECUTION / SECOND RUN" right="PROOF P5 + P6" color={COLORS.blue} />
      <Cursor progress={easeOut(frame, 0, 30)} />
      <div style={safe}>
        <div
          style={{
            position: "absolute",
            top: 110,
            fontSize: 88,
            fontWeight: 950,
            lineHeight: 0.95,
            letterSpacing: -5,
          }}
        >
          补上 proof
          <br />
          <span style={{color: COLORS.blue}}>再跑一次</span>
        </div>
        <div
          style={{
            position: "absolute",
            top: 410,
            left: 0,
            right: 0,
            height: 600,
            background: COLORS.ink,
            borderRadius: 30,
            padding: 34,
            color: COLORS.white,
            boxShadow: `22px 24px 0 ${COLORS.lilac}`,
          }}
        >
          <div style={{display: "flex", gap: 12, marginBottom: 30}}>
            {[COLORS.red, "#FFD34D", COLORS.green].map((color) => (
              <div key={color} style={{width: 20, height: 20, borderRadius: "50%", background: color}} />
            ))}
          </div>
          <div style={{fontFamily: MONO, fontSize: 22, lineHeight: 1.7}}>
            <div style={{color: COLORS.lilac}}>$ python validate_project.py --phase preproduction</div>
            <div style={{marginTop: 18}}>claims&nbsp;&nbsp; {passed.summary.claims}</div>
            <div>beats&nbsp;&nbsp;&nbsp; {passed.summary.beats}</div>
            <div>scenes&nbsp;&nbsp; {passed.summary.scenes}</div>
            <div>assets&nbsp;&nbsp; {passed.summary.assets}</div>
            <div style={{marginTop: 24, color: COLORS.green, fontSize: 48, fontWeight: 950}}>
              {passed.status.toUpperCase()}
            </div>
          </div>
          <div
            style={{
              position: "absolute",
              right: 28,
              bottom: 28,
              padding: "14px 20px",
              borderRadius: 99,
              background: COLORS.green,
              color: COLORS.ink,
              fontFamily: MONO,
              fontWeight: 950,
              fontSize: 20,
              transform: `scale(${interpolate(status, [0, 1], [0.4, 1])})`,
            }}
          >
            BLOCKED → PASSED
          </div>
        </div>
        <div style={{position: "absolute", top: 1080, left: 0, right: 0}}>
          <div
            style={{
              fontFamily: MONO,
              fontSize: 20,
              fontWeight: 900,
              color: COLORS.blue,
              marginBottom: 20,
            }}
          >
            REMOTION / ONE FINAL TIMELINE
          </div>
          {[
            ["VOICE", COLORS.blue],
            ["CAPTIONS", COLORS.red],
            ["VISUAL", COLORS.green],
          ].map(([label, color], index) => (
            <div
              key={label}
              style={{
                display: "grid",
                gridTemplateColumns: "150px 1fr",
                alignItems: "center",
                gap: 20,
                marginBottom: 18,
                fontFamily: MONO,
                fontSize: 19,
                fontWeight: 900,
              }}
            >
              <span>{label}</span>
              <div style={{height: 24, background: "rgba(11,16,32,.13)", overflow: "hidden"}}>
                <div
                  style={{
                    width: `${interpolate(timeline, [0, 1], [0, 100 - index * 5])}%`,
                    height: "100%",
                    background: color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const CloseScene: React.FC = () => {
  const frame = useCurrentFrame();
  const reveal = easeOut(frame, 0, 30);
  return (
    <AbsoluteFill style={{background: COLORS.white, color: COLORS.ink, fontFamily: FONT}}>
      <Kicker left="ACCEPTANCE / VIEWER CAN EXPLAIN IT" right="DONE" color={COLORS.blue} />
      <Cursor progress={reveal} />
      <div style={safe}>
        <div
          style={{
            position: "absolute",
            top: 170,
            left: 0,
            right: 0,
            height: 370,
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 18,
          }}
        >
          <div style={{background: "#E8E8E8", padding: 30, borderRadius: 28}}>
            <div style={{fontFamily: MONO, fontSize: 19, fontWeight: 900}}>OLD</div>
            <div style={{fontSize: 52, fontWeight: 950, marginTop: 36}}>文案</div>
            <div style={{height: 4, background: COLORS.ink, margin: "18px 0"}} />
            <div style={{fontSize: 52, fontWeight: 950, opacity: 0.28}}>装饰画</div>
          </div>
          <div
            style={{
              background: COLORS.ink,
              color: COLORS.white,
              padding: 30,
              borderRadius: 28,
              transform: `translateY(${interpolate(reveal, [0, 1], [80, 0])}px)`,
            }}
          >
            <div style={{fontFamily: MONO, fontSize: 19, color: COLORS.green, fontWeight: 900}}>
              NEW
            </div>
            <div style={{fontSize: 52, fontWeight: 950, marginTop: 36}}>主张</div>
            <div style={{height: 4, background: COLORS.green, margin: "18px 0"}} />
            <div style={{fontSize: 52, fontWeight: 950, color: COLORS.green}}>真实证据</div>
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            top: 720,
            left: 0,
            right: 0,
            fontSize: 142,
            lineHeight: 0.9,
            fontWeight: 950,
            letterSpacing: -9,
          }}
        >
          听懂
          <br />
          <span style={{color: COLORS.blue}}>还要看见</span>
        </div>
        <div
          style={{
            position: "absolute",
            top: 1180,
            left: 0,
            right: 0,
            borderTop: `4px solid ${COLORS.ink}`,
            paddingTop: 30,
            fontFamily: MONO,
            fontSize: 24,
            lineHeight: 1.5,
            fontWeight: 800,
          }}
        >
          TASK → INPUT → PROCESS → RESULT
          <br />
          CLAIM → PROOF → SAME MOMENT
        </div>
      </div>
    </AbsoluteFill>
  );
};

const CaptionPhrase: React.FC<{caption: Caption}> = ({caption}) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, 0, 8);
  const terms = /(proof|blocked|passed|Remotion|证据|模板|任务|输入|执行|结果)/gi;
  const parts = caption.text.split(terms);
  return (
    <div
      style={{
        position: "absolute",
        left: 58,
        right: 142,
        bottom: 74,
        minHeight: 118,
        background: "rgba(11,16,32,.94)",
        borderTop: `6px solid ${COLORS.green}`,
        padding: "22px 28px 18px",
        color: COLORS.white,
        fontFamily: FONT,
        fontSize: 44,
        lineHeight: 1.34,
        fontWeight: 900,
        zIndex: 100,
        boxShadow: "0 16px 48px rgba(0,0,0,.35)",
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [18, 0])}px)`,
      }}
    >
      {parts.map((part, index) => {
        const highlighted = terms.test(part);
        terms.lastIndex = 0;
        return (
          <span
            key={`${index}-${part}`}
            style={{color: highlighted ? COLORS.green : COLORS.white, whiteSpace: "pre"}}
          >
            {part}
          </span>
        );
      })}
    </div>
  );
};

const Captions: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const {delayRender, continueRender, cancelRender} = useDelayRender();
  const [handle] = useState(() => delayRender("load captions"));
  const fetchCaptions = useCallback(async () => {
    try {
      const response = await fetch(staticFile("data/captions.json"));
      if (!response.ok) {
        throw new Error(`captions request failed: ${response.status}`);
      }
      const data = (await response.json()) as Caption[];
      setCaptions(data);
      continueRender(handle);
    } catch (error) {
      cancelRender(error instanceof Error ? error : new Error(String(error)));
    }
  }, [cancelRender, continueRender, handle]);
  useEffect(() => {
    void fetchCaptions();
  }, [fetchCaptions]);
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      {(captions ?? []).map((caption, index) => {
        const from = Math.max(0, Math.round((caption.startMs / 1000) * fps));
        const durationInFrames = Math.max(
          1,
          Math.round(((caption.endMs - caption.startMs) / 1000) * fps),
        );
        return (
          <Sequence key={`${caption.startMs}-${index}`} from={from} durationInFrames={durationInFrames}>
            <CaptionPhrase caption={caption} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const SCENE_COMPONENTS = [
  HookScene,
  InputScene,
  PipelineScene,
  DirectorScene,
  PassScene,
  CloseScene,
];

export const FreeDirectorToolVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: COLORS.ink}}>
      {storyboard.scenes.map((scene, index) => {
        const Component = SCENE_COMPONENTS[index];
        const from = Math.round(scene.start * fps);
        const durationInFrames = Math.max(1, Math.round((scene.end - scene.start) * fps));
        return (
          <Sequence key={scene.id} from={from} durationInFrames={durationInFrames}>
            <Component />
          </Sequence>
        );
      })}
      <Audio src={staticFile("audio/narration.mp3")} />
      <Captions />
    </AbsoluteFill>
  );
};
