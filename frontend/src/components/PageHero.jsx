import { Reveal } from './Reveal'

export function PageHero({ eyebrow, title, subtitle, size = 'sm', children }) {
  return (
    <div className={`page-hero page-hero-${size}`}>
      <div className="page-hero-bg" aria-hidden="true" />

      <div className="page-hero-inner">
        <Reveal className="page-hero-content">
          {eyebrow && <p className="page-hero-eyebrow">{eyebrow}</p>}
          <h1>{title}</h1>
          {subtitle && <p className="page-hero-subtitle">{subtitle}</p>}
          {children}
        </Reveal>
      </div>
    </div>
  )
}
