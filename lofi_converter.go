package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"time"
)

func check(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "usage: lofi-converter <youtube url>")
		os.Exit(1)
	}
	url := os.Args[1]

	tmpDir, err := ioutil.TempDir("", "lofi")
	check(err)
	defer os.RemoveAll(tmpDir)

	inputPath := filepath.Join(tmpDir, "input.m4a")

	// Create output directory if it doesn't exist
	outputDir := "output"
	err = os.MkdirAll(outputDir, 0755)
	check(err)

	// Use timestamp to create unique filename
	timestamp := time.Now().Format("20060102_150405")
	outputPath := filepath.Join(outputDir, fmt.Sprintf("lofi_%s.mp3", timestamp))

	// Download audio using yt-dlp
	cmdYt := exec.Command("yt-dlp", "-f", "bestaudio", "-o", inputPath, url)
	cmdYt.Stdout = os.Stdout
	cmdYt.Stderr = os.Stderr
	err = cmdYt.Run()
	check(err)

	// Lofi filter chain for ffmpeg
	filter := "atempo=0.9,lowpass=f=5000,highpass=f=150,aecho=0.8:0.9:1000:0.3"

	cmdFfmpeg := exec.Command("ffmpeg", "-y", "-i", inputPath, "-af", filter, outputPath)
	cmdFfmpeg.Stdout = os.Stdout
	cmdFfmpeg.Stderr = os.Stderr
	err = cmdFfmpeg.Run()
	check(err)

	fmt.Println(outputPath)
}
