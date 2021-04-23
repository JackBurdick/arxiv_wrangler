aw() {
    cur_env=$(echo $CONDA_DEFAULT_ENV)
    echo 'activate arxiv'
    conda activate arxiv
    cd '/Users/leakymosfet/dev/github/arxiv_wrangler/src'
    python main.py $1
    cd -
    conda activate $cur_env
    echo 'done arxiv_wrangle'
}