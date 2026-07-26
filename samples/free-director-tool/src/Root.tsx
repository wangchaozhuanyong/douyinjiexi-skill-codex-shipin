import {Composition} from "remotion";
import storyboard from "../storyboard.json";
import {FreeDirectorToolVideo} from "./Video";

const fps = storyboard.fps;
const durationInFrames = Math.ceil(
  storyboard.scenes[storyboard.scenes.length - 1].end * fps,
);

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="FreeDirectorTool"
      component={FreeDirectorToolVideo}
      durationInFrames={durationInFrames}
      fps={fps}
      width={storyboard.width}
      height={storyboard.height}
    />
  );
};
