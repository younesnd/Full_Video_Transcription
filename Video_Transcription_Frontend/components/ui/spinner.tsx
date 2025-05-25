// components/ui/spinner.tsx
import { Loader2 } from "lucide-react";

export function Spinner({ className = "h-5 w-5" }: { className?: string }) {
  return (
    <Loader2 className={`animate-spin text-muted-foreground ${className}`} />
  );
}
