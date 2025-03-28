package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var stopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Stop KeyFort Server",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Stopped!")
	},
}

func init() {
	rootCmd.AddCommand(stopCmd)
}
