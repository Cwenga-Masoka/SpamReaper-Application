function StatusMessage({ message, children }) {
    return (
      <div
        role="status"
        className="flex flex-col items-center gap-3 py-10 text-center text-sm text-on-surface-variant"
      >
        <p>{message}</p>
        {children}
      </div>
    )
  }
  
  export default StatusMessage