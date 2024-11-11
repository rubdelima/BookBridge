import git

def gerar_gitflow_mermaid(caminho_repo):
    try:
        repo = git.Repo(caminho_repo)
        commits = list(repo.iter_commits('--all', reverse=True))

        mermaid = "gitGraph\n"
        branch_atual = repo.active_branch.name
        branches_criadas = set()

        for commit in commits:
            mensagem = commit.message.split('\n')[0].replace("\"", "'")
            
            for ref in repo.refs:
                branch_name = ref.name.replace('origin/', '')
                if ref.commit == commit and branch_name not in branches_criadas:
                    if branch_name == 'main':
                        mermaid += f"    checkout main\n"
                    else:
                        mermaid += f"    branch {branch_name}\n"
                        if branch_name == branch_atual:
                            mermaid += f"    checkout {branch_name}\n"
                    branches_criadas.add(branch_name)

            mermaid += f"    commit id:\"{mensagem[:20]}\"\n"

            if len(commit.parents) > 1:
                mermaid += f"    merge {commit.parents[1].hexsha[:7]} id:\"MERGE\"\n"

        return mermaid

    except Exception as e:
        return f"Erro ao gerar o diagrama: {str(e)}"

caminho_repo = '.'

diagrama_mermaid = gerar_gitflow_mermaid(caminho_repo)
print(diagrama_mermaid)