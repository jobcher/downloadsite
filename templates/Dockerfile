FROM ubuntu:latest
RUN apt-get update && apt-get install -y nginx openssh-server
RUN mkdir -p /run/sshd
RUN echo "root:sanjiang666" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22 80 443
CMD ["/usr/sbin/sshd", "-D"]