import "./globals.css";

import { cn } from "@/lib/utils";
import { Montserrat } from "next/font/google";
import { MyRuntimeProvider } from "./MyRuntimeProvider";
import { Suspense } from "react";
import { TooltipProvider } from "@/components/ui/tooltip"

const montserrat = Montserrat({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <MyRuntimeProvider>
      <html lang="en">
        <body className={cn(montserrat.className, "h-dvh")}>
          <Suspense><TooltipProvider>{children}</TooltipProvider></Suspense>
        </body>
      </html>
    </MyRuntimeProvider>
  );
}
