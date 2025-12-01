package com.topai.incidenciasestacionamiento.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table (name = "usuarios")
public class Usuario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(unique = true)
    private String correo;
    private String password;
    private String nombre;
    private String role = "ROLE_USER";
    @OneToOne(mappedBy = "usuario")
    private Propietario propietario;

}
