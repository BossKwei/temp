// Fill out your copyright notice in the Description page of Project Settings.


#include "Demo1_FPPMineCube.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "ConstructorHelpers.h"

// Sets default values
ADemo1_FPPMineCube::ADemo1_FPPMineCube()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = false;

	//
	UBoxComponent *CollisionComp = CreateDefaultSubobject<UBoxComponent>(TEXT("BoxComp"));
	CollisionComp->InitBoxExtent(FVector(25.0f, 25.0f, 25.0f));
	RootComponent = CollisionComp;

	// Create and position a mesh component so we can see where our cube is
	UStaticMeshComponent* CubeVisual = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VisualRepresentation"));
	CubeVisual->SetupAttachment(RootComponent);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereVisualAsset(TEXT("/Game/StarterContent/Shapes/Shape_Cube.Shape_Cube"));
	if (SphereVisualAsset.Succeeded())
	{
		CubeVisual->SetStaticMesh(SphereVisualAsset.Object);
	}

	// Do not simulate physics
	CubeVisual->SetSimulatePhysics(false);
}

// Called when the game starts or when spawned
void ADemo1_FPPMineCube::BeginPlay()
{
	Super::BeginPlay();
}

// Called every frame
void ADemo1_FPPMineCube::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}
