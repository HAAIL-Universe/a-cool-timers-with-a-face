import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useUrgencyStyle } from '../hooks/useUrgencyStyle';

describe('useUrgencyStyle', () => {
  it('returns safe green style when urgency is low', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'low', colourIntensity: { r: 0, g: 255, b: 0 } })
    );

    expect(result.current.backgroundColor).toBe('rgb(0, 255, 0)');
    expect(result.current.transition).toBe('background-color 500ms ease-in-out');
    expect(result.current.className).not.toContain('pulse');
  });

  it('returns caution yellow style when urgency is medium', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'medium', colourIntensity: { r: 255, g: 255, b: 0 } })
    );

    expect(result.current.backgroundColor).toBe('rgb(255, 255, 0)');
    expect(result.current.transition).toBe('background-color 500ms ease-in-out');
    expect(result.current.className).not.toContain('pulse');
  });

  it('returns urgent orange style when urgency is high', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'high', colourIntensity: { r: 255, g: 136, b: 0 } })
    );

    expect(result.current.backgroundColor).toBe('rgb(255, 136, 0)');
    expect(result.current.transition).toBe('background-color 500ms ease-in-out');
    expect(result.current.className).not.toContain('pulse');
  });

  it('returns critical red style with pulse class when urgency is critical', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'critical', colourIntensity: { r: 255, g: 0, b: 0 } })
    );

    expect(result.current.backgroundColor).toBe('rgb(255, 0, 0)');
    expect(result.current.transition).toBe('background-color 500ms ease-in-out');
    expect(result.current.className).toContain('urgency-pulse');
  });

  it('handles interpolated RGB values correctly', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'high', colourIntensity: { r: 200, g: 100, b: 50 } })
    );

    expect(result.current.backgroundColor).toBe('rgb(200, 100, 50)');
  });

  it('clamps RGB values to 0-255 range', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'low', colourIntensity: { r: 300, g: -10, b: 128 } })
    );

    expect(result.current.backgroundColor).toBe('rgb(255, 0, 128)');
  });

  it('applies transition consistently across all urgency levels', () => {
    const urgencies: Array<'low' | 'medium' | 'high' | 'critical'> = ['low', 'medium', 'high', 'critical'];

    urgencies.forEach((urgency) => {
      const { result } = renderHook(() =>
        useUrgencyStyle({ urgencyLevel: urgency, colourIntensity: { r: 100, g: 100, b: 100 } })
      );

      expect(result.current.transition).toBe('background-color 500ms ease-in-out');
    });
  });

  it('only applies pulse class when urgency is critical', () => {
    const nonCriticalUrgencies: Array<'low' | 'medium' | 'high'> = ['low', 'medium', 'high'];

    nonCriticalUrgencies.forEach((urgency) => {
      const { result } = renderHook(() =>
        useUrgencyStyle({ urgencyLevel: urgency, colourIntensity: { r: 100, g: 100, b: 100 } })
      );

      expect(result.current.className).not.toContain('pulse');
    });
  });

  it('returns object with backgroundColor, transition, and className properties', () => {
    const { result } = renderHook(() =>
      useUrgencyStyle({ urgencyLevel: 'medium', colourIntensity: { r: 255, g: 255, b: 0 } })
    );

    expect(result.current).toHaveProperty('backgroundColor');
    expect(result.current).toHaveProperty('transition');
    expect(result.current).toHaveProperty('className');
    expect(typeof result.current.backgroundColor).toBe('string');
    expect(typeof result.current.transition).toBe('string');
    expect(typeof result.current.className).toBe('string');
  });
});
