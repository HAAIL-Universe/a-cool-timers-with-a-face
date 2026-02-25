import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FacialAvatar } from '../components/FacialAvatar';

describe('FacialAvatar', () => {
  it('renders calm expression for safe urgency level', () => {
    const { container } = render(
      <FacialAvatar expression="calm" urgencyLevel="low" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-calm');
  });

  it('renders concerned expression for caution urgency level', () => {
    const { container } = render(
      <FacialAvatar expression="concerned" urgencyLevel="medium" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-concerned');
  });

  it('renders stressed expression for urgent urgency level', () => {
    const { container } = render(
      <FacialAvatar expression="stressed" urgencyLevel="high" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-stressed');
  });

  it('renders critical expression for critical urgency level', () => {
    const { container } = render(
      <FacialAvatar expression="critical" urgencyLevel="critical" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-critical');
  });

  it('applies pulse class only when isPulsing is true', () => {
    const { container, rerender } = render(
      <FacialAvatar expression="calm" urgencyLevel="low" isPulsing={false} />
    );
    let grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).not.toHaveClass('pulse');

    rerender(
      <FacialAvatar expression="calm" urgencyLevel="low" isPulsing={true} />
    );
    grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('pulse');
  });

  it('applies pulse class when urgencyLevel is critical', () => {
    const { container } = render(
      <FacialAvatar expression="critical" urgencyLevel="critical" isPulsing={true} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('pulse');
    expect(grid).toHaveClass('expression-critical');
  });

  it('renders 16x16 pixel grid layout', () => {
    const { container } = render(
      <FacialAvatar expression="calm" urgencyLevel="low" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('facial-grid');
    const pixels = grid?.querySelectorAll('[data-testid^="pixel-"]');
    expect(pixels?.length).toBe(256);
  });

  it('updates expression when expression prop changes', () => {
    const { container, rerender } = render(
      <FacialAvatar expression="calm" urgencyLevel="low" isPulsing={false} />
    );
    let grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-calm');

    rerender(
      <FacialAvatar expression="concerned" urgencyLevel="medium" isPulsing={false} />
    );
    grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-concerned');
    expect(grid).not.toHaveClass('expression-calm');
  });

  it('applies urgency color tint to pixel grid', () => {
    const { container } = render(
      <FacialAvatar expression="calm" urgencyLevel="low" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('urgency-low');
  });

  it('applies urgency color tint for medium level', () => {
    const { container } = render(
      <FacialAvatar expression="concerned" urgencyLevel="medium" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('urgency-medium');
  });

  it('applies urgency color tint for high level', () => {
    const { container } = render(
      <FacialAvatar expression="stressed" urgencyLevel="high" isPulsing={false} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('urgency-high');
  });

  it('applies urgency color tint for critical level', () => {
    const { container } = render(
      <FacialAvatar expression="critical" urgencyLevel="critical" isPulsing={true} />
    );
    const grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('urgency-critical');
  });

  it('maintains correct expression class through urgency transitions', () => {
    const { container, rerender } = render(
      <FacialAvatar expression="concerned" urgencyLevel="low" isPulsing={false} />
    );
    let grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-concerned');
    expect(grid).toHaveClass('urgency-low');

    rerender(
      <FacialAvatar expression="concerned" urgencyLevel="critical" isPulsing={true} />
    );
    grid = container.querySelector('[data-testid="facial-grid"]');
    expect(grid).toHaveClass('expression-concerned');
    expect(grid).toHaveClass('urgency-critical');
    expect(grid).toHaveClass('pulse');
  });
});
