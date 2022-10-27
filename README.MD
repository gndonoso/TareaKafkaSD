creación de topicos y modificación de particiones

kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 2 --topic Stock
kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 2 --topic NuevoMiembro
kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 2 --topic NuevaVenta
kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 2 --topic Ubicacion
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic NuevoMiembro --partitions 2
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic NuevaVenta --partitions 2
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic Ubicacion --partitions 2
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic Stock --partitions 2
