import { getInitial } from '../utils/text'

function Avatar({ name, imageUrl }) {
  const initial = getInitial(name)

  return (
    <div className="rounded-full p-0.5 ring-2 ring-primary-fixed/80">
      {imageUrl ? (
        <img
          src={imageUrl}
          alt={`${name}'s profile`}
          className="h-8 w-8 rounded-full object-cover"
        />
      ) : (
        <div
          role="img"
          aria-label={name}
          className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-fixed text-sm font-bold text-on-primary-fixed"
        >
          {initial}
        </div>
      )}
    </div>
  )
}

export default Avatar