FROM hashicorp/terraform:latest  

WORKDIR /terraform  

COPY  main.tf .  

# add aws cli location to path
#ENV PATH=~/.local/bin/terraform:$PATH
ENV PATH="/usr/local/bin/terraform:${PATH}"

ENTRYPOINT ["terraform"]   