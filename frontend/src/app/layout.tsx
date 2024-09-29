import type { Metadata } from "next";
import localFont from "next/font/local";
import { Card, CardBody } from "@nextui-org/react";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Login Page for HeadCount",
  description: "Login to access the HeadCount dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
          <Card className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
            <CardBody className="bg-white p-8 rounded-md shadow-md text-center w-full sm:w-96">
              {children}
            </CardBody>
          </Card>
        </div>
      </body>
    </html>
  );
}
