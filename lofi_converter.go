package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
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
        wavPath := filepath.Join(tmpDir, "output.wav")

        // Download audio using yt-dlp
        cmdYt := exec.Command("yt-dlp", "-f", "bestaudio", "-o", inputPath, url)
        cmdYt.Stdout = os.Stdout
        cmdYt.Stderr = os.Stderr
        err = cmdYt.Run()
        check(err)

        // Convert to wav for note extraction
        cmdFfmpeg := exec.Command("ffmpeg", "-y", "-i", inputPath, "-ac", "1", "-ar", "44100", wavPath)
        cmdFfmpeg.Stdout = os.Stdout
        cmdFfmpeg.Stderr = os.Stderr
        err = cmdFfmpeg.Run()
        check(err)

        fmt.Println(wavPath)
}
