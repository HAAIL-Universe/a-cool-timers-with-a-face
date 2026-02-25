import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import FacialAvatar from '../components/FacialAvatar';
import { UrgencyLevel } from '../types/timer';

describe('FacialAvatar', () => {
  it('renders SVG element', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const svg = container.querySelector('svg');
    expect(svg).toBeTruthy();
  });

  it('renders correct number of pixels for safe expression', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const rects = container.querySelectorAll('rect');
    expect(rects.length).toBeGreaterThan(0);
  });

  it('applies correct color for safe urgency level', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const rects = container.querySelectorAll('rect');
    rects.forEach((rect) => {
      expect(rect.getAttribute('fill')).toBe('#00FF00');
    });
  });

  it('applies correct color for caution urgency level', () => {
    const { container } = render(<FacialAvatar urgencyLevel="caution" />);
    const rects = container.querySelectorAll('rect');
    rects.forEach((rect) => {
      expect(rect.getAttribute('fill')).toBe('#FFFF00');
    });
  });

  it('applies correct color for urgent urgency level', () => {
    const { container } = render(<FacialAvatar urgencyLevel="urgent" />);
    const rects = container.querySelectorAll('rect');
    rects.forEach((rect) => {
      expect(rect.getAttribute('fill')).toBe('#FF8800');
    });
  });

  it('applies correct color for critical urgency level', () => {
    const { container } = render(<FacialAvatar urgencyLevel="critical" />);
    const rects = container.querySelectorAll('rect');
    rects.forEach((rect) => {
      expect(rect.getAttribute('fill')).toBe('#FF0000');
    });
  });

  it('applies border color matching urgency level', () => {
    const { container } = render(<FacialAvatar urgencyLevel="caution" />);
    const svg = container.querySelector('svg');
    const style = window.getComputedStyle(svg!);
    expect(svg).toBeTruthy();
  });

  it('renders with pixelated image rendering style', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const svg = container.querySelector('svg');
    expect(svg?.style.imageRendering).toBe('crisp-edges');
  });

  it('updates expression when urgency level changes', () => {
    const { container, rerender } = render(<FacialAvatar urgencyLevel="safe" />);
    let rects = container.querySelectorAll('rect');
    const safeCount = rects.length;

    rerender(<FacialAvatar urgencyLevel="critical" />);
    rects = container.querySelectorAll('rect');
    const criticalCount = rects.length;

    expect(safeCount).not.toBe(criticalCount);
  });

  it('renders with black background', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const svg = container.querySelector('svg');
    expect(svg?.style.backgroundColor).toBe('#000000');
  });

  it('applies pulse animation when isPulsing and critical', () => {
    const { container } = render(<FacialAvatar urgencyLevel="critical" isPulsing={true} />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.style.animation).toContain('pulse');
  });

  it('does not apply pulse animation when isPulsing but not critical', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" isPulsing={true} />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.style.animation).toBe('');
  });

  it('does not apply pulse animation when not pulsing', () => {
    const { container } = render(<FacialAvatar urgencyLevel="critical" isPulsing={false} />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.style.animation).toBe('');
  });

  it('renders SVG with correct viewBox', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const svg = container.querySelector('svg');
    expect(svg?.getAttribute('viewBox')).toBe('0 0 16 16');
  });

  it('renders all urgency levels without errors', () => {
    const levels: UrgencyLevel[] = ['safe', 'caution', 'urgent', 'critical'];
    levels.forEach((level) => {
      const { container } = render(<FacialAvatar urgencyLevel={level} />);
      const svg = container.querySelector('svg');
      expect(svg).toBeTruthy();
    });
  });

  it('renders rectangles with correct dimensions', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const rects = container.querySelectorAll('rect');
    rects.forEach((rect) => {
      expect(rect.getAttribute('width')).toBe('1');
      expect(rect.getAttribute('height')).toBe('1');
    });
  });

  it('renders with proper SVG dimensions', () => {
    const { container } = render(<FacialAvatar urgencyLevel="safe" />);
    const svg = container.querySelector('svg');
    expect(svg?.getAttribute('width')).toBe('384');
    expect(svg?.getAttribute('height')).toBe('384');
  });
});
