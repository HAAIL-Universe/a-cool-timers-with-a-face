import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useUrgencyStyle } from '../hooks/useUrgencyStyle';

describe('useUrgencyStyle', () => {
  it('returns green background for low urgency', () => {
    const { result } = renderHook(() => useUrgencyStyle('low'));
    expect(result.current.backgroundColor).toBe('#00FF00');
    expect(result.current.className).not.toContain('pulse');
  });

  it('returns yellow background for medium urgency', () => {
    const { result } = renderHook(() => useUrgencyStyle('medium'));
    expect(result.current.backgroundColor).toBe('#FFFF00');
    expect(result.current.className).not.toContain('pulse');
  });

  it('returns orange background for high urgency', () => {
    const { result } = renderHook(() => useUrgencyStyle('high'));
    expect(result.current.backgroundColor).toBe('#FF8800');
    expect(result.current.className).not.toContain('pulse');
  });

  it('returns red background with pulse class for critical urgency', () => {
    const { result } = renderHook(() => useUrgencyStyle('critical'));
    expect(result.current.backgroundColor).toBe('#FF0000');
    expect(result.current.className).toContain('urgency-pulse');
  });

  it('includes transition property in style object', () => {
    const { result } = renderHook(() => useUrgencyStyle('low'));
    expect(result.current.transition).toBeDefined();
    expect(result.current.transition).toBe('background-color 500ms ease-in-out');
  });

  it('handles urgency level changes with transition', () => {
    const { result, rerender } = renderHook(
      ({ urgency }) => useUrgencyStyle(urgency),
      { initialProps: { urgency: 'low' as const } }
    );

    expect(result.current.backgroundColor).toBe('#00FF00');

    rerender({ urgency: 'critical' as const });
    expect(result.current.backgroundColor).toBe('#FF0000');
    expect(result.current.className).toContain('urgency-pulse');
  });

  it('returns correct className without pulse for non-critical states', () => {
    const { result: lowResult } = renderHook(() => useUrgencyStyle('low'));
    const { result: mediumResult } = renderHook(() => useUrgencyStyle('medium'));
    const { result: highResult } = renderHook(() => useUrgencyStyle('high'));

    expect(lowResult.current.className).toBe('urgency-background');
    expect(mediumResult.current.className).toBe('urgency-background');
    expect(highResult.current.className).toBe('urgency-background');
  });

  it('applies pulse class only for critical urgency', () => {
    const { result: criticalResult } = renderHook(() => useUrgencyStyle('critical'));
    expect(criticalResult.current.className).toBe('urgency-background urgency-pulse');
  });

  it('maintains consistent return object structure', () => {
    const { result } = renderHook(() => useUrgencyStyle('medium'));
    expect(result.current).toHaveProperty('backgroundColor');
    expect(result.current).toHaveProperty('className');
    expect(result.current).toHaveProperty('transition');
  });

  describe('color mapping edge cases', () => {
    it('maps low urgency to exact green hex code', () => {
      const { result } = renderHook(() => useUrgencyStyle('low'));
      expect(result.current.backgroundColor).toMatch(/^#[0-9A-F]{6}$/i);
      expect(result.current.backgroundColor.toUpperCase()).toBe('#00FF00');
    });

    it('maps critical urgency to exact red hex code', () => {
      const { result } = renderHook(() => useUrgencyStyle('critical'));
      expect(result.current.backgroundColor.toUpperCase()).toBe('#FF0000');
    });
  });
});
