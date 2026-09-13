Output "/Users/avik/git_projects/github/starship-theme/media/iterm2.gif"

Set Shell "zsh"
Set FontFamily "JetBrainsMono Nerd Font Mono"
Set FontSize 16
Set Width 1200
Set Height 300
Set Theme "Dracula"
Set TypingSpeed 20ms
Set Padding 20

Type "export STARSHIP_CONFIG='/Users/avik/git_projects/github/starship-theme/themes/iterm2.toml' STARSHIP_LOG=error"
Enter
Sleep 200ms

Type 'eval "$(starship init zsh)"'
Enter
Sleep 500ms

Hide
Type "clear"
Enter
Sleep 300ms
Show

Type "echo 'iterm2'"
Enter
Sleep 600ms
