package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var startCmd = &cobra.Command{
	Use:   "start",
	Short: "Prints hello message",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Hello from Cobra!")
	},
}

func init() {
	rootCmd.AddCommand(startCmd)
}
