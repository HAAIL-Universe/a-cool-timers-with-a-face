import { describe, it, expect } from 'vitest';
import { intensityToColour, intensityToBackground } from '../utils/colour';

describe('intensityToColour', () => {
  it('returns pure green at intensity 0.0', () => {
    const result = intensityToColour(0.0);
    expect(result).toBe('#00FF00');
  });

  it('returns pure yellow at intensity 0.5', () => {
    const result = intensityToColour(0.5);
    expect(result).toBe('#FFFF00');
  });

  it('returns pure red at intensity 1.0', () => {
    const result = intensityToColour(1.0);
    expect(result).toBe('#FF0000');
  });

  it('returns green-yellow gradient at 0.25', () => {
    const result = intensityToColour(0.25);
    expect(result).toBe('#7FFF00');
  });

  it('returns yellow-red gradient at 0.75', () => {
    const result = intensityToColour(0.75);
    expect(result).toBe('#FF7F00');
  });

  it('clamps values below 0.0 to green', () => {
    const resultNegative = intensityToColour(-0.5);
    const resultZero = intensityToColour(0.0);
    expect(resultNegative).toBe(resultZero);
    expect(resultNegative).toBe('#00FF00');
  });

  it('clamps values above 1.0 to red', () => {
    const resultHigh = intensityToColour(1.5);
    const resultOne = intensityToColour(1.0);
    expect(resultHigh).toBe(resultOne);
    expect(resultHigh).toBe('#FF0000');
  });

  it('returns uppercase hex strings', () => {
    const result = intensityToColour(0.5);
    expect(result).toMatch(/^#[0-9A-F]{6}$/);
  });

  it('handles mid-range green-to-yellow values', () => {
    const result10 = intensityToColour(0.1);
    const result40 = intensityToColour(0.4);
    expect(result10).toBe('#33FF00');
    expect(result40).toBe('#CCFF00');
  });

  it('handles mid-range yellow-to-red values', () => {
    const result60 = intensityToColour(0.6);
    const result90 = intensityToColour(0.9);
    expect(result60).toBe('#FF99FF');
    expect(result90).toBe('#FF1900');
  });

  it('always has blue component at 0', () => {
    const intensities = [0, 0.25, 0.5, 0.75, 1.0];
    intensities.forEach(intensity => {
      const result = intensityToColour(intensity);
      const blueHex = result.slice(4, 6);
      expect(blueHex).toBe('00');
    });
  });

  it('always has red component at or above 128 for intensity >= 0.25', () => {
    const result = intensityToColour(0.25);
    const redHex = result.slice(1, 3);
    const redValue = parseInt(redHex, 16);
    expect(redValue).toBeGreaterThanOrEqual(128);
  });

  it('always has green component at or above 128 for intensity <= 0.75', () => {
    const result = intensityToColour(0.75);
    const greenHex = result.slice(3, 5);
    const greenValue = parseInt(greenHex, 16);
    expect(greenValue).toBeGreaterThanOrEqual(128);
  });

  it('handles floating point precision near boundaries', () => {
    const result50 = intensityToColour(0.5);
    const result50Plus = intensityToColour(0.50001);
    expect(result50).toBe('#FFFF00');
    expect(result50Plus).toBe('#FFFF00');
  });

  it('produces consistent output for same input', () => {
    const intensity = 0.42;
    const result1 = intensityToColour(intensity);
    const result2 = intensityToColour(intensity);
    expect(result1).toBe(result2);
  });
});

describe('intensityToBackground', () => {
  it('returns gradient string for intensity 0.0', () => {
    const result = intensityToBackground(0.0);
    expect(result).toContain('linear-gradient(135deg,');
    expect(result).toContain('#00FF00');
    expect(result).toContain('33 0%');
    expect(result).toContain('22 100%');
  });

  it('returns gradient string for intensity 0.5', () => {
    const result = intensityToBackground(0.5);
    expect(result).toContain('linear-gradient(135deg,');
    expect(result).toContain('#FFFF00');
    expect(result).toContain('33 0%');
    expect(result).toContain('22 100%');
  });

  it('returns gradient string for intensity 1.0', () => {
    const result = intensityToBackground(1.0);
    expect(result).toContain('linear-gradient(135deg,');
    expect(result).toContain('#FF0000');
    expect(result).toContain('33 0%');
    expect(result).toContain('22 100%');
  });

  it('includes colour with 33% opacity at start', () => {
    const result = intensityToBackground(0.5);
    const expected = '#FFFF0033';
    expect(result).toContain(expected);
  });

  it('includes colour with 22% opacity at end', () => {
    const result = intensityToBackground(0.5);
    const expected = '#FFFF0022';
    expect(result).toContain(expected);
  });

  it('applies intensity clamping through colour function', () => {
    const resultNegative = intensityToBackground(-1.0);
    const resultZero = intensityToBackground(0.0);
    expect(resultNegative).toBe(resultZero);
  });

  it('applies 135deg diagonal gradient for all intensities', () => {
    const intensities = [0.0, 0.3, 0.5, 0.7, 1.0];
    intensities.forEach(intensity => {
      const result = intensityToBackground(intensity);
      expect(result).toMatch(/linear-gradient\(135deg,/);
    });
  });

  it('produces valid CSS gradient syntax', () => {
    const result = intensityToBackground(0.5);
    expect(result).toMatch(
      /linear-gradient\(135deg, #[0-9A-F]{8} 0%, #[0-9A-F]{8} 100%\)/
    );
  });
});
