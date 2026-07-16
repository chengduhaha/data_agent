import { SettingsNav } from "@/components/SettingsNav";

export default function SettingsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-3 md:flex-row">
      <SettingsNav />
      <div className="panel min-h-[70vh] flex-1 overflow-auto p-5 md:p-6">
        {children}
      </div>
    </div>
  );
}
