"use client";

import { useState } from "react";
import Image from "next/image";
import { Card, CardBody, Button } from "@nextui-org/react";

export default function Login() {
  const [errorMessage, setErrorMessage] = useState("");

  const handleLoginClick = async () => {
    setErrorMessage(""); // Reset error message

    // Perform login check
    window.location.href = "http://localhost:8000/auth/login/google";
  };

  return (
    <Card className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
      <CardBody className="bg-white p-8 rounded-md shadow-md text-center w-full sm:w-96">
        {/* Logo */}
        <Image
          src="/images/logo.png"
          alt="HeadCount"
          width={96}
          height={96}
          className="mx-auto h-24 w-auto"
        />
        <h1 className="text-2xl font-bold mt-4">Sign in to HeadCount</h1>
        <p className="text-gray-500 text-sm mt-2">
          Welcome back! Please sign in to view the dashboard.
        </p>

        {/* Render Error Message */}
        {errorMessage && (
          <div className="text-red-500 text-sm mt-4 mb-4 p-2 bg-red-100 rounded-md">
            {errorMessage}
          </div>
        )}

        <div className="mt-6 space-y-4">
          {/* Login Button */}
          <Button
            onClick={handleLoginClick}
            color="warning"
            className="w-full py-2"
          >
            Login with Google
          </Button>
        </div>

        {/* "Forgot Password?" and "Sign Up" Links */}
        <div className="mt-4 text-sm text-gray-600">
          Don&apos;t have an account?&nbsp;
          <a href="/register" className="hover:underline">
            Contact Sales
          </a>
        </div>
      </CardBody>
    </Card>
  );
}
