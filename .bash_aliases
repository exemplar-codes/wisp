
# sanjarcode/vtt Add to .bash_aliases or .zsh_aliases
# I'm using pnpm
function vtt() {
    WISP_BE_PORT=8301
    WISP_FE_PORT=8302

    fuser -k "$WISP_BE_PORT/tcp"
    fuser -k "$WISP_FE_PORT/tcp"

    PORT="$WISP_BE_PORT" pnpm --prefix ~/.sanjarcode-vtt/wisp start &
    pnpm --prefix ~/.sanjarcode-vtt/wisp-fe run dev --port "$WISP_FE_PORT" --open
}
