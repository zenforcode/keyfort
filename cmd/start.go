package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var (
	port string
	host string
)

var startCmd = &cobra.Command{
	Use:   "start",
	Short: "Start KeyFort Server",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Starting KeyFort Server at %s:%s\n", host, port)
	},
}

func init() {
	startCmd.Flags().StringVarP(&port, "port", "p", "8080", "Port to run the server on")
	startCmd.Flags().StringVarP(&host, "host", "", "0.0.0.0", "Host to bind the server to")
	rootCmd.AddCommand(startCmd)
}
