aw() {
    echo 'activate arxiv'
    conda activate arxiv
    cd '/Users/leakymosfet/dev/github/arxiv_wrangler/src'
    python main.py $1
    cd -
    echo 'done arxiv_wrangle'
}