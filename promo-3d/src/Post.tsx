import React, { useLayoutEffect, useMemo } from 'react';
import { useThree } from '@react-three/fiber';
import { continueRender, delayRender, useCurrentFrame } from 'remotion';
import {
  BloomEffect, DepthOfFieldEffect, EffectComposer, EffectPass, NoiseEffect, RenderPass, SMAAEffect,
  ToneMappingEffect, ToneMappingMode, VignetteEffect, BlendFunction,
} from 'postprocessing';
import * as THREE from 'three';
import { isReady } from './kit';

/** Renders the scene once per Remotion frame (ThreeCanvas has no render loop), after every asset is ready:
 * depth of field focused on a world point, bloom for the gold neon, AgX tone mapping, vignette, light grain. */
export const Post: React.FC<{ focus: THREE.Vector3; bokeh: number; bloom: number }> = ({ focus, bokeh, bloom }) => {
  const { gl, scene, camera, size } = useThree();
  const frame = useCurrentFrame();
  const fx = useMemo(() => {
    gl.toneMapping = THREE.NoToneMapping;
    gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
    const composer = new EffectComposer(gl, { frameBufferType: THREE.HalfFloatType, multisampling: 4 });
    composer.addPass(new RenderPass(scene, camera));
    const dof = new DepthOfFieldEffect(camera, { worldFocusRange: 0.6, bokehScale: 2.5 });
    const bloomFx = new BloomEffect({ intensity: 1, luminanceThreshold: 0.92, luminanceSmoothing: 0.2, mipmapBlur: true, radius: 0.7 });
    const tone = new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL });
    const vignette = new VignetteEffect({ darkness: 0.45, offset: 0.35 });
    const noise = new NoiseEffect({ blendFunction: BlendFunction.OVERLAY }); noise.blendMode.opacity.value = 0.12;
    composer.addPass(new EffectPass(camera, dof));
    composer.addPass(new EffectPass(camera, bloomFx, tone, vignette, new SMAAEffect()));
    return { composer, dof, bloomFx };
  }, [gl, scene, camera]);
  useLayoutEffect(() => { fx.composer.setSize(size.width, size.height); }, [fx, size]);
  useLayoutEffect(() => {
    const h = delayRender('post ' + frame);
    let tries = 0;
    const draw = () => {
      if (!isReady() && tries++ < 600) { requestAnimationFrame(draw); return; }
      fx.dof.target = focus.clone();
      fx.dof.bokehScale = bokeh;
      fx.bloomFx.intensity = bloom;
      fx.composer.render();
      continueRender(h);
    };
    requestAnimationFrame(() => requestAnimationFrame(draw));
  }, [frame, fx, focus, bokeh, bloom]);
  return null;
};
