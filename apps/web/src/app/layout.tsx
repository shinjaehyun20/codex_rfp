import "./globals.css";
import { TopNav } from "../components/TopNav";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <TopNav />
        <div className="container">{children}</div>
      </body>
    </html>
  );
}
