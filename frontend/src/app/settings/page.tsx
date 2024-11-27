"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button,
  Input,
  Card,
  CardBody,
} from "@nextui-org/react";
import Image from "next/image";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";

export default function Settings() {
  const [maxOccupancy, setMaxOccupancy] = useState(0);
  const [selectedFeedType, setSelectedFeedType] = useState("live");
  const [selectedWebcam, setSelectedWebcam] = useState("default");
  const [youtubeURL, setYoutubeURL] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [username, setUsername] = useState<string | undefined>(undefined);
  const router = useRouter();

  useEffect(() => {
    const token = Cookies.get("session_token");
    if (token) {
      const decodedToken = jwtDecode(token);
      setUsername(decodedToken.sub);
    }
  }, []);

  const handleSaveSettings = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    // Validate maxOccupancy before saving
    if (maxOccupancy < 0) {
      setErrorMessage("Max Occupancy cannot be less than 0");
      return;
    }

    // If validation passes, reset error message and proceed
    setErrorMessage("");

    // Store settings (example using local storage)
    localStorage.setItem("maxOccupancy", maxOccupancy.toString());
    localStorage.setItem("selectedFeedType", selectedFeedType);

    if (selectedFeedType === "live") {
      router.push("/dashboard");
    } else {
      router.push("/video_dashboard");
      localStorage.setItem("youtubeURL", youtubeURL);

      try {
        // Send the YouTube URL to the backend if feed type is prerecorded
        await axios.post("http://localhost:8000/process_feed", {
          url: youtubeURL,
        });

        alert("Video URL successfully sent to the backend!");
      } catch (error) {
        console.error("Error sending video URL:", error);
        alert("Failed to send video URL to the backend.");
      }
    }
  };

  const handleMaxOccupancyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = Number(e.target.value);
    if (value >= 0) {
      setMaxOccupancy(value);
      setErrorMessage(""); // Clear error message if valid
    } else {
      setErrorMessage("Max Occupancy cannot be less than 0");
    }
  };

  const handleSignOut = async () => {
    Cookies.remove("session_token");
    router.push("/");
  };

  return (
    <Card className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
      <CardBody className="bg-white p-8 rounded-md shadow-md text-center w-full sm:w-96">
        <div className="flex justify-between items-center mb-4">
          <div>
            <p className="text-sm">Signed in as: {username}</p>
          </div>
          <Button onClick={handleSignOut} color="danger" size="sm">
            Sign Out
          </Button>
        </div>

        <Image
          src="/images/logo.png"
          alt="HeadCount"
          width={96}
          height={96}
          className="mx-auto h-24 w-auto"
        />

        <h1 className="text-3xl font-bold text-center">Settings</h1>

        <form
          onSubmit={handleSaveSettings}
          className="flex flex-col gap-4 items-center justify-center sm:items-start w-full"
        >
          {/* Max Occupancy Input */}
          <b></b>
          <div className="w-full">
            <label className="block text-sm font-medium mb-2 text-left">
              Enter maximum occupancy:
            </label>
            <Input
              label="Max Occupancy"
              type="number"
              value={maxOccupancy.toString()}
              onChange={handleMaxOccupancyChange}
              className="mt-1 p-2 w-full"
              min={0}
              required
            />
          </div>

          {/* Error Message */}
          {errorMessage && (
            <p className="text-red-500 text-sm mt-1 text-center">
              {errorMessage}
            </p>
          )}

          {/* Select Feed Type Dropdown */}
          <div className="w-full">
            <label className="block text-sm font-medium mb-2 text-left">
              Select Feed Type:
            </label>
            <div className="flex justify-center">
              <Dropdown>
                <DropdownTrigger>
                  <Button variant="bordered" className="w-full">
                    {selectedFeedType === "live"
                      ? "Live Feed"
                      : "Pre-recorded Feed"}
                  </Button>
                </DropdownTrigger>
                <DropdownMenu
                  aria-label="Select Feed Type"
                  disallowEmptySelection
                  selectionMode="single"
                  variant="flat"
                  onAction={(key) => setSelectedFeedType(key.toString())}
                  className="dropdown-width"
                >
                  <DropdownItem key="live">Live Feed</DropdownItem>
                  <DropdownItem key="prerecorded">
                    Pre-recorded Feed
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </div>
          </div>

          {/* Conditionally Render Live Feed Webcam Dropdown */}
          {selectedFeedType === "live" && (
            <div className="w-full">
              <label className="block text-sm font-medium mb-2 text-left">
                Please select your preferred webcam:
              </label>
              <div className="flex justify-center">
                <Dropdown>
                  <DropdownTrigger>
                    <Button variant="bordered" className="w-full">
                      {selectedWebcam === "default"
                        ? "Select Webcam"
                        : selectedWebcam}
                    </Button>
                  </DropdownTrigger>
                  <DropdownMenu
                    aria-label="Select Webcam"
                    disallowEmptySelection
                    selectionMode="single"
                    variant="flat"
                    onAction={(key) => setSelectedWebcam(key.toString())}
                    className="dropdown-width"
                  >
                    <DropdownItem key="default">Same as System</DropdownItem>
                    <DropdownItem key="webcam1">
                      FaceTime HD Camera
                    </DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </div>
            </div>
          )}

          {/* Conditionally Render YouTube URL Input */}
          {selectedFeedType === "prerecorded" && (
            <div className="w-full">
              <label
                htmlFor="youtubeURL"
                className="block text-sm font-medium text-left mb-1 "
              >
                YouTube URL
              </label>
              {/* Styled YouTube URL Input */}
              <Input
                type="text"
                id="youtubeURL"
                value={youtubeURL}
                onChange={(e) => setYoutubeURL(e.target.value)}
                className="w-full"
                placeholder="Enter YouTube video URL"
                required
                classNames={{
                  inputWrapper: "input-wrapper-styles",
                  input: "input-styles",
                }}
              />
            </div>
          )}

          {/* Save Button */}
          <Button
            type="submit"
            className="mt-6 px-4 py-2 w-full"
            color="warning"
          >
            Start
          </Button>
        </form>

        <style jsx>{`
          .dropdown-width {
            width: 100%;
          }
          .input-wrapper-styles {
            @apply mt-1;
          }
          .input-styles {
            @apply p-2 border rounded focus:outline-none focus:ring focus:border-blue-300;
          }
        `}</style>
      </CardBody>
    </Card>
  );
}