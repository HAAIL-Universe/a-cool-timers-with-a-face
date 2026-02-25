function intensityToColour(intensity: number): string {
  const clamped = Math.max(0, Math.min(1, intensity));

  let r: number, g: number, b: number;

  if (clamped <= 0.5) {
    // Green (0, 255, 0) to Yellow (255, 255, 0)
    const ratio = clamped / 0.5; // 0 to 1
    r = Math.round(255 * ratio);
    g = 255;
    b = 0;
  } else {
    // Yellow (255, 255, 0) to Red (255, 0, 0)
    const ratio = (clamped - 0.5) / 0.5; // 0 to 1
    r = 255;
    g = Math.round(255 * (1 - ratio));
    b = 0;
  }

  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
}

function intensityToBackground(intensity: number): string {
  const colour = intensityToColour(intensity);
  return `linear-gradient(135deg, ${colour}33 0%, ${colour}22 100%)`;
}

export { intensityToColour, intensityToBackground };
