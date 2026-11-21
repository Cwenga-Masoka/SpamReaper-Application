import Avatar from './Avatar'
import Icon from './Icon'
import {
  APP_LOGO_ICON,
  APP_NAME,
  APP_TAGLINE,
  SCREEN_BADGE_LABEL,
} from '../constants/branding'

function Header({ userName, avatarUrl }) {
  return (
    <header className="fixed inset-x-0 top-0 z-50 bg-surface/90 pt-[env(safe-area-inset-top,0px)] shadow-[0_4px_20px_-2px_rgba(70,115,78,0.05)] backdrop-blur-xl">
      <div className="flex h-25 items-center justify-between px-4">
        <div className="flex items-center gap-5">
          <Icon name={APP_LOGO_ICON} className="text-3xl text-primary" />
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-1.5">
              <span className="text-3xl font-semibold tracking-tight text-primary">
                {APP_NAME}
              </span>
              <span className="rounded-full bg-primary-fixed px-1.5 py-0.5 text-[19px] font-bold text-on-primary-fixed">
                {SCREEN_BADGE_LABEL}
              </span>
            </div>
            <span className="text-lg text-outline">{APP_TAGLINE}</span>
          </div>
        </div>
        <Avatar name={userName} imageUrl={avatarUrl} />
      </div>
    </header>
  )
}

export default Header