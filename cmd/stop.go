package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var stopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Stop keyvault-server",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Stopped!")
	},
}

func init() {
	rootCmd.AddCommand(stopCmd)
}
